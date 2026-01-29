import asyncio

from agents import OpenAIConversationsSession, Runner
from agents.exceptions import (
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)

from ai_agents import research_agent
from utility_functions import fix_youtube_links


async def run_with_guardrail(
    user_input: str | None, session: OpenAIConversationsSession
) -> str | None:
    try:
        result = await Runner.run(
            research_agent, user_input, max_turns=20, session=session
        )
        print("=== Run complete ===")
        return result.final_output
    except InputGuardrailTripwireTriggered as e:
        print(f"[BLOCKED] {e.guardrail_result.output.output_info}")
        return f"I cannot answer that because: {e.guardrail_result.output.output_info}"
    except OutputGuardrailTripwireTriggered as e:
        print(f"[BLOCKED] {e.guardrail_result.output.output_info}")
        return f"I cannot answer that because: {e.guardrail_result.output.output_info}"


async def fetch_results(
    user_input: str, session: OpenAIConversationsSession
) -> tuple[str, tuple[str, list[str]]]:
    result = await run_with_guardrail(user_input=user_input, session=session)
    if result is None:
        msg = "Your question was blocked by guardrails."
        return msg, (msg, [])

    # Check if the result indicates a block (simple string check for now, or we could have returned a structured object)
    if result.startswith("I cannot answer that because:"):
        return result, (result, [])

    video_links = fix_youtube_links(result)
    print(f"Video links: {video_links} ######")
    return result, video_links


if __name__ == "__main__":
    session = OpenAIConversationsSession()
    query = "What is trauma? and how to counter traunma?"
    result, videos = asyncio.run(fetch_results(user_input=query, session=session))
