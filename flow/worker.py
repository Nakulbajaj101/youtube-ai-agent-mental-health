import asyncio
from concurrent.futures import ThreadPoolExecutor

from activities import (
    ElasticSearchActivities,
    YouTubeTranscriptActivities,
    get_videos_metadata,
)
from create_indices import ElasticSearchClient
from temporalio.client import Client
from temporalio.worker import Worker
from workflow import PodcastTranscriptWorkflow


async def run_podcast_worker():
    client = await Client.connect("localhost:7233")

    executor = ThreadPoolExecutor(max_workers=8)

    yt_activities = YouTubeTranscriptActivities()
    es_activities = ElasticSearchActivities(
        host="http://localhost:9200", index_name="podcasts"
    )
    es_search_activity = ElasticSearchClient(
        host="http://localhost:9200", index_name="podcasts"
    )

    worker = Worker(
        client=client,
        task_queue="podcast_transcript_task_queue",
        workflows=[PodcastTranscriptWorkflow],
        activities=[
            get_videos_metadata,
            es_search_activity.create_indices,
            yt_activities.preprocess_transcript,
            es_activities.create_index,
        ],
        activity_executor=executor,
    )

    await worker.run()


if __name__ == "__main__":
    asyncio.run(run_podcast_worker())
