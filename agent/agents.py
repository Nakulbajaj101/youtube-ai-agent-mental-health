from config import research_instructions, summarization_instructions
from pydantic_ai.agent import Agent
from tools import ElasticsearchCLient

summarization_agent = Agent(
    name="summarization",
    instructions=summarization_instructions,
    model="openai:gpt-4o-mini",
)

es = ElasticsearchCLient(summarize_agent=summarization_agent)

research_agent = Agent(
    name="research",
    instructions=research_instructions,
    model="openai:gpt-4o-mini",
    tools=[es.search_videos, es.summarize],
)
