# Research Agent 🕵️‍♂️

This directory contains the AI Research Agent that queries the ingested YouTube transcripts to answer user questions.

## Overview

The agent is built using `pydantic-ai` and follows a sophisticated **Deep Research** pattern (ReAct). It executes a multi-stage reasoning process:
1.  **Stage 1: Initial Exploration**: The agent performs broad search queries to understand the topic's landscape, key definitions, and major themes.
2.  **Stage 2: Deep Investigation**: It executes refined, deep-dive queries to find specific mechanisms, case studies, and technical details.

It has access to tools that allow it to:
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

### 3. Run the Streamlit App (UI)
For a richer experience with a UI and embedded video playback:

```bash
uv run streamlit run app.py
```

This will launch a web interface at `http://localhost:8501`.

## Key Files

*   **`app.py`**: Streamlit application with chat interface and video embedding logic.
*   **`main.py`**: Entry point for checking agent logic via CLI.
*   **`agents.py`**: Initializes the `research_agent` and `summarization_agent`.
*   **`tools.py`**: Defines the `ElasticsearchCLient` class which provides the `search_videos` and `summarize` tools.
*   **`utility_functions.py`**: Helper functions (e.g., `fix_youtube_links`).
