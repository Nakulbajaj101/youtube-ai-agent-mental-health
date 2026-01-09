# Ingestion Flow 🌊

This directory contains the Temporal workflow and activities responsible for ingesting YouTube video data into Elasticsearch.

## Overview

The flow is designed to:
1.  **Fetch Metadata**: Retrieve video titles and URLs from a predefined list.
2.  **Create Indices**: Initialize the Elasticsearch index (`self_improvement_podcasts`) with correct mappings (analyzers, stop words, etc.).
3.  **Process Transcripts**: For each video:
    *   Download the transcript from YouTube.
    *   Preprocess the text (clean and format).
    *   Index the content into Elasticsearch as document chunks.

## Data Source

The list of videos to be processed is defined in `data.py`. 
To add more videos, simply append to the `data` list in `data.py`:

```python
data = [
    {"title": "Video Title", "url": "https://www.youtube.com/watch?v=VIDEO_ID"},
    ...
]
```

## Running the Flow

### 1. Install Dependencies

Ensure you are in the `flow` directory and have `uv` installed.

```bash
uv sync
```

### 2. Start the Worker

The worker listens for tasks from the Temporal server.

```bash
uv run worker.py
```

### 3. Execute the Workflow

In a separate terminal, trigger the workflow execution.

```bash
uv run workflow.py
```

## Key Files

*   **`workflow.py`**: Defines the `PodcastTranscriptWorkflow` orchestrator.
*   **`worker.py`**: Configures and runs the Temporal Worker.
*   **`activities.py`**: Implements the actual business logic (activities) for fetching and indexing.
*   **`config.py`**: Contains Elasticsearch index settings and mappings.
*   **`create_indices.py`**: Helper to create the ES index.
