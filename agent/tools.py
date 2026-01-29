import json

from config import ELASTIC_SEARCH_API_KEY, ELASTIC_SEARCH_HOST
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import (
    BadRequestError,
    ConnectionError,
    NotFoundError,
    RequestError,
)
from pydantic_ai import Agent, RunContext
from agents import Runner


class ElasticsearchCLient:
    def __init__(self, summarize_agent: Agent, index_name: str):
        self._host = ELASTIC_SEARCH_HOST
        self.summarize_agent = summarize_agent
        self.index_name = index_name
        if ELASTIC_SEARCH_API_KEY:
            self.__key = ELASTIC_SEARCH_API_KEY
            self._client = Elasticsearch(hosts=self._host, api_key=self.__key)
        else:
            self._client = Elasticsearch(hosts=self._host)

    async def search_videos(self, query: str, size: int = 5) -> list[dict]:
        """
        Performs a full-text search across video titles and subtitles using Elasticsearch.

        This function utilizes a 'multi_match' query with a 'best_fields' type. It prioritizes
        matches found in the title over subtitles and applies a custom English analyzer.

        Args:
            query (str): The search terms provided by the user.
            size (int, optional): The maximum number of search results to return.
                Defaults to 5.

        Returns:
            list: A list of dictionaries containing highlighted snippets and the
                associated 'video_id'. Returns an empty list if an error occurs.

        Example:
            >>> results = search_videos("machine learning", size=1)
            >>> print(results)
            [
                {
                    'title': ['Intro to *Machine Learning*'],
                    'subtitles': ['In this video, we discuss *machine learning* basics...'],
                    'video_id': 'vid_001'
                }
            ]

        Raises:
            ElasticsearchException: Logged internally, returns empty list on failure.
        """

        body = {
            "size": size,
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^3", "subtitles"],
                    "type": "best_fields",
                    "analyzer": "my_english_analyzer",
                }
            },
            "highlight": {
                "pre_tags": ["*"],
                "post_tags": ["*"],
                "fields": {
                    "title": {"fragment_size": 150, "number_of_fragments": 1},
                    "subtitles": {
                        "fragment_size": 150,
                        "number_of_fragments": 3,
                        "order": "score",
                    },
                },
            },
        }

        try:
            response = self._client.search(index=self.index_name, body=body)
            hits = response.body["hits"]["hits"]

            results = []
            for hit in hits:
                # Safely get highlights; default to empty dict if no matches found in fields
                highlight = hit.get("highlight", {})
                highlight["video_id"] = hit["_id"]
                results.append(highlight)
                return results

        except NotFoundError:
            print(f"Error: Index '{self.index_name}' not found.")
        except ConnectionError:
            print("Error: Could not connect to Elasticsearch.")
        except RequestError as e:
            print(f"Error: Invalid search request. {e}")
        except BadRequestError as e:
            print(
                f"Error: Request not rightly configured or sent, please check again. {e}"
            )
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return []

    def get_subtitles_by_id(self, video_id: str) -> dict:
        """Function to help receive video transcripts from the elasticsearch

        Args:
            video_id (str): The youtube video id for which user can request subtitles"

        Returns:
            dict: A dictionary with video id, title of the video and its subtitles
        """

        result = self._client.get(index="self_improvement_podcasts", id=video_id)
        return result["_source"]

    async def summarize(self, ctx: RunContext, video_id: str) -> str:
        """
        Generate a summary for a video based on the conversation history,
        search queries, and the video's subtitles.
        """
        user_queries = []
        search_queries = []

        for m in ctx.messages:
            for p in m.parts:
                kind = p.part_kind
                if kind == "user-prompt":
                    user_queries.append(p.content)
                elif kind == "tool-call":
                    if p.tool_name == "search_videos":
                        args = json.loads(p.args)
                        query = args["query"]
                        search_queries.append(query)
        subtitles = self.get_subtitles_by_id(video_id=video_id)["subtitles"]
        prompt = f"""
            user query:
            {"\n".join(user_queries)}
            
            search engine queries: 
            {"\n".join(search_queries)}
            
            subtitles:
            {subtitles}
            """
        summary_result = await self.summarize_agent.run(prompt)
        return summary_result.output
    
    async def summarise_video(self, video_id: str) -> str:
        """
        Extracts transcript for a given video ID and uses a sub-agent to summarize it.
        Returns the summary.
        """
        subtitles = self.get_subtitles_by_id(video_id=video_id)["subtitles"]
        prompt = f"""Transcript: {subtitles}"""
        summary_result = await Runner.run(self.summarize_agent, input=prompt)
        return summary_result.final_output
