# Research Agent 🕵️‍♂️

This directory contains the AI Research Agent that queries the ingested YouTube transcripts to answer user questions.

## Overview

The agent is built using `pydantic-ai` and follows a ReAct (Reasoning + Acting) pattern. It has access to tools that allow it to:
*   **Search**: Query the Elasticsearch index for relevant video segments.
*   **Summarize**: Generate summaries of specific video content.
*   **Answer**: Synthesize findings into a coherent answer with verified citations (YouTube timestamps).

## Configuration

The agent's behavior and environment are configured in `config.py` and via environment variables.

### Environment Variables

*   `OPENAI_API_KEY`: **Required**. Your OpenAI API key.
*   `ELASTIC_SEARCH_HOST`: The URL of your Elasticsearch instance (default: `http://localhost:9200`).
*   `ELASTIC_SEARCH_API_KEY`: API key for Elasticsearch (optional, if your instance requires auth).

### Config File (`config.py`)

*   **`research_instructions`**: The system prompt that governs the Research Agent's behavior (ReAct steps, citation rules).
*   **`summarization_instructions`**: The prompt for the summarization sub-agent.

## Usage

### 1. Install Dependencies

Ensure you are in the `agent` directory.

```bash
uv sync
```

### 2. Run the Agent

You can run the agent using the provided `main.py` script. 

```bash
uv run main.py
```

By default, `main.py` runs a hardcoded query ("What is trauma? and how to counter traunma?"). You can modify the `query` variable in `main.py` to ask different questions.

```python
if __name__ == "__main__":
    query = "Your custom question here"
    result = asyncio.run(fetch_results(query=query))
    print(result)
```

## Key Files

*   **`agents.py`**: Initializes the `research_agent` and `summarization_agent`.
*   **`tools.py`**: Defines the `ElasticsearchCLient` class which provides the `search_videos` and `summarize` tools.
*   **`main.py`**: Entry point for running the agent.
*   **`utility_functions.py`**: Helper functions (e.g., `fix_youtube_links`).
