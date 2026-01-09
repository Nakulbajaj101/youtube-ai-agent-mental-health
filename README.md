# YouTube AI Research Agent: Mental Health & Self-Improvement 🎥�

This project implements an advanced **Deep Research Agent** that digests and understands YouTube video transcripts to answer complex user questions with high-quality citations.

The system focuses on a curated dataset of **Mental Health and Self-Improvement** content, featuring renowned experts like **Dr. Gabor Maté**, **Mel Robbins**, **Dr. Andrew Huberman**, **Trevor Noah**, and others. It is designed to provide users with deep, actionable insights on topics such as trauma, anxiety, ADHD, relationships, and leadership.

It consists of two main components:
1.  **Flow (`/flow`)**: A robust data ingestion pipeline orchestrated by [Temporal](https://temporal.io/). It handles the ETL process: fetching video metadata, downloading transcripts, preprocesses text, and indexing rich vector embeddings into Elasticsearch.
2.  **Agent (`/agent`)**: A **Deep Research Agent** built with `pydantic-ai` that goes beyond simple RAG. It employs a multi-stage **ReAct (Reasoning + Acting)** workflow to:
    *   **Explore**: Perform broad initial searches to understand the topic landscape.
    *   **Investigate**: Execute targeted, deep-dive queries to find specific mechanisms, case studies, and scientific details.
    *   **Synthesize**: Combine findings into comprehensive answers with precise, clickable YouTube timestamp citations.

## Key Features
*   **Deep Research Capabilities**: Unlike standard chatbots, this agent uses a multi-step reasoning process (Initial Exploration -> Deep Investigation) to ensure answers are thorough and nuanced.
*   **Mental Health Focus**: Specialized knowledge base built from top-tier self-improvement, psychology, and neuroscience podcasts.
*   **Verifiable Citations**: Every claim is backed by a direct link to the exact moment in the video where it was discussed.
*   **Interactive UI**: A "Calm/Headspace" inspired Streamlit interface for a mindful research experience.

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

**Run the Agent (CLI):**
```bash
uv run main.py
```

**Run the Streamlit App (UI):**
```bash
uv run streamlit run app.py
```
*Access the UI at http://localhost:8501*

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