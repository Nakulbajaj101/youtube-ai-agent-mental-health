from agents import Agent, ModelSettings, function_tool

from config import (INDEX_NAME, research_instructions,
                    summarization_instructions)
from guardrails import safety_guardrail, topic_guardrail
from tools import ElasticsearchCLient

summarization_agent = Agent(
    name="summarization",
    instructions=summarization_instructions,
    model="gpt-4o-mini",
)

es = ElasticsearchCLient(summarize_agent=summarization_agent, index_name=INDEX_NAME)

research_agent = Agent(
    name="research",
    instructions=research_instructions,
    model="gpt-4o-mini",
    model_settings=ModelSettings(max_tokens=4000, temperature=0, parallel_tool_calls=True),
    tools=[function_tool(es.search_videos), function_tool(es.summarise_video)],
    input_guardrails=[topic_guardrail],
    output_guardrails=[safety_guardrail],
)
