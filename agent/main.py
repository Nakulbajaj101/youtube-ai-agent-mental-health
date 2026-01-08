import asyncio

from agents import research_agent
from utility_functions import fix_youtube_links


async def fetch_results(query: str) -> str:
    result = await research_agent.run(query)
    clean_result = fix_youtube_links(result.output)
    return clean_result


if __name__ == "__main__":
    query = "What is trauma? and how to counter traunma?"
    result = asyncio.run(fetch_results(query=query))
    print(result)
