from agents import (Agent, GuardrailFunctionOutput, Runner, input_guardrail,
                    output_guardrail)
from pydantic import BaseModel

from config import output_guardrail_instructions, topic_guardrail_instructions


class GuardrailOutput(BaseModel):
    fail: bool
    reasoning: str

topic_guardrail_agent = Agent(
    name="topic_guardrail",
    instructions=topic_guardrail_instructions,
    model="gpt-4o-mini",
    output_type=GuardrailOutput,
)

safety_guardrail_agent = Agent(
    name="safety_guardrail",
    instructions=output_guardrail_instructions,
    model="gpt-4o-mini",
    output_type=GuardrailOutput,
)

@input_guardrail
async def topic_guardrail(ctx, agent, input_info):
    """Check if question is about Health and wellbeing, and self improvement"""
    
    result = await Runner.run(topic_guardrail_agent, input_info)
    output = result.final_output
    return GuardrailFunctionOutput(
        output_info=output.reasoning,
        tripwire_triggered=output.fail
    )

@output_guardrail
async def safety_guardrail(ctx, agent, agent_output):
    """Check if the response is about Health and wellbeing, and self improvement"""
    
    guardrail_input = f"Agent responded with {agent_output}"
    result = await Runner.run(safety_guardrail_agent, guardrail_input)
    output = result.final_output
    return GuardrailFunctionOutput(
        output_info=output.reasoning,
        tripwire_triggered=output.fail
    )
