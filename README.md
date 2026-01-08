# YouTube AI Agent 🎥🤖

This project implements an AI-powered agentic workflow that digests YouTube video transcripts, indexes them into Elasticsearch, and provides a Research Agent to answer questions based on the video content.

It consists of two main components:
1.  **Flow (`/flow`)**: A data ingestion pipeline orchestrated by [Temporal](https://temporal.io/). It fetches video metadata, downloads transcripts, preprocesses them, and indexes them into Elasticsearch.
2.  **Agent (`/agent`)**: A Research Agent built with `pydantic-ai` that queries the Elasticsearch index to answer user questions with citations and timestamps.

## Prerequisites

Before running the project, ensure you have the following installed:

*   **Python 3.12+** (Managed by `uv` is recommended)
*   **[uv](https://github.com/astral-sh/uv)** (Fast Python package installer and resolver)
*   **[Temporal CLI](https://docs.temporal.io/cli)** (For running the Temporal server locally)
*   **[Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)** (Running locally on port 9200)

## Quick Start 🚀

### 1. Setup Environment

Clone the repository and navigate to the project root:

```bash
git clone <repository_url>
cd youtube-ai-agent
```

### 2. Start Infrastructure

Make sure your local Temporal and Elasticsearch servers are running.

**Temporal:**
```bash
temporal server start-dev
```
*The Temporal UI will be available at http://localhost:8233 (or the port specified).*

**Elasticsearch:**
Ensure Elasticsearch is running on `http://localhost:9200`.

### 3. Run the Ingestion Flow

Navigate to the `flow` directory to install dependencies and run the worker and workflow.

```bash
cd flow
uv sync
```

**Start the Worker:**
In one terminal:
```bash
uv run worker.py
```

**Execute the Workflow:**
In another terminal:
```bash
uv run workflow.py
```
This will ingest the videos defined in `flow/data.py` into Elasticsearch.

### 4. Run the Research Agent

Navigate to the `agent` directory:

```bash
cd ../agent
uv sync
```

**Configure Environment:**
Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```
*(Optionally set `ELASTIC_SEARCH_HOST` if it's not localhost)*

**Run the Agent:**
```bash
uv run main.py
```

## Directory Structure

*   **`flow/`**: Contains the Temporal workflow definitions, activities, and data for ingestion.
    *   `workflow.py`: Defines the `PodcastTranscriptWorkflow`.
    *   `worker.py`: Runs the Temporal worker.
    *   `activities.py`: Contains the logic for fetching transcripts and indexing.
    *   `data.py`: List of YouTube videos to process.
*   **`agent/`**: Contains the Research Agent implementation.
    *   `agents.py`: Defines the `research_agent` and `summarization_agent`.
    *   `tools.py`: Elasticsearch tools for the agent.
    *   `main.py`: Entry point to run the agent.

## License

[MIT](LICENSE)