import asyncio
from unittest.mock import MagicMock, patch
import sys

# Add current dir to path
sys.path.append(".")

from main import fetch_results, OpenAIConversationsSession


async def test_guardrail_returned_string():
    print("Testing fetch_results handling of blocked string...")
    session = MagicMock(spec=OpenAIConversationsSession)

    # We patch run_with_guardrail to simulate the caught exception outcome
    # This avoids needing to mock the exact Exception class from external library
    with patch("main.run_with_guardrail") as mock_run:
        blocked_msg = "I cannot answer that because: Violation of topic"
        mock_run.return_value = blocked_msg

        result, videos = await fetch_results("test", session)

        print(f"Result: {result}")
        print(f"Videos: {videos}")

        assert result == blocked_msg
        # Expect videos to be (msg, []) as per my fix
        assert videos == (blocked_msg, [])
        print(
            "SUCCESS: Blocked string handled correctly and structure matches app.py expectations."
        )


if __name__ == "__main__":
    asyncio.run(test_guardrail_returned_string())
