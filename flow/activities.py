import os

from config import ELASTIC_SEARCH_API_KEY, ELASTIC_SEARCH_HOST
from elasticsearch import Elasticsearch
from temporalio import activity
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig


def configure_proxy() -> GenericProxyConfig:
    proxy_user = os.getenv("proxy_user")
    proxy_pass = os.getenv("proxy_pass")
    proxy_base_url = os.getenv("proxy_base_url")
    proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_base_url}"

    proxy_config = GenericProxyConfig(http_url=proxy_url, https_url=proxy_url)

    return proxy_config


def format_timestamp(seconds: float) -> str:
    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours == 0:
        return f"{minutes}:{secs:02}"
    return f"{hours}:{minutes:02}:{secs:02}"


def make_subtitles(transcript: str) -> str:
    lines = []
    for entry in transcript:
        ts = format_timestamp(entry.start)
        text = entry.text.replace("\n", " ")
        lines.append(ts + " " + text)

    return "\n".join(lines)


@activity.defn
def get_videos_metadata(data: list[dict]) -> list:
    videos = []
    for dt in data:
        _, video_id = dt["url"].split("watch?v=")
        dt["video_id"] = video_id
        videos.append(dt)
    print(f"Will process {len(videos)} videos")
    return videos


class ElasticSearchActivities:
    def __init__(self, index_name: str):
        self._host = ELASTIC_SEARCH_HOST
        if ELASTIC_SEARCH_API_KEY:
            self.__key = ELASTIC_SEARCH_API_KEY
            self._client = Elasticsearch(hosts=self._host, api_key=self.__key)
        else:
            self._client = Elasticsearch(hosts=self._host)
        self.index_name = index_name

    def video_exists(self, video_id: str):
        resp = self._client.exists(index=self.index_name, id=video_id)
        return resp.body

    @activity.defn
    def create_index(self, video_data: dict, subtitles: str):
        if not self.video_exists(video_data["video_id"]):
            doc = {
                "video_id": video_data["video_id"],
                "title": video_data["title"],
                "subtitles": subtitles,
            }
            self._client.index(index=self.index_name, id=doc["video_id"], document=doc)
        else:
            print(f"Index already exists for video {video_data['video_id']}.")


class YouTubeTranscriptActivities:
    def __init__(self, use_proxy: bool = True):
        if use_proxy:
            self._proxy_config = configure_proxy()
        else:
            self._proxy_config = None

        self._ytt_api = YouTubeTranscriptApi(proxy_config=self._proxy_config)

    def fetch_transcript(self, video_id):
        return self._ytt_api.fetch(video_id)

    @activity.defn
    def preprocess_transcript(self, video_id):
        transcript = self.fetch_transcript(video_id=video_id)
        subtitles = make_subtitles(transcript=transcript)
        return subtitles
