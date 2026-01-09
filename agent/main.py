import asyncio

from agents import research_agent
from utility_functions import fix_youtube_links


from pydantic_ai.messages import ModelMessage


async def fetch_results(
    query: str, message_history: list[ModelMessage] | None = None
) -> tuple[str, list[ModelMessage]]:
    result = await research_agent.run(query, message_history=message_history)
    clean_result = fix_youtube_links(result.output)
    return clean_result, result.new_messages()


if __name__ == "__main__":
    query = "What is trauma? and how to counter traunma?"
    result, history = asyncio.run(fetch_results(query=query))
    print(result)
