import asyncio
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import (
        ElasticSearchActivities,
        YouTubeTranscriptActivities,
        get_videos_metadata,
    )
    from create_indices import ElasticSearchClient

from data import data
from temporalio.client import Client


@workflow.defn
class PodcastTranscriptWorkflow:
    @workflow.run
    async def workflow(self, data: list[dict] = data):
        workflow.logger.info(f"starting workflow for videos {len(data)}")

        videos = await workflow.execute_activity(
            activity=get_videos_metadata,
            args=(data,),
            start_to_close_timeout=timedelta(minutes=1),
        )

        await workflow.execute_activity(
            activity=ElasticSearchClient.create_indices,
            args=(),
            start_to_close_timeout=timedelta(seconds=10),
        )

        for video in videos:
            video_id = video["video_id"]

            subtitles = await workflow.execute_activity(
                activity=YouTubeTranscriptActivities.preprocess_transcript,
                args=(video_id,),
                start_to_close_timeout=timedelta(minutes=10),
            )

            await workflow.execute_activity(
                activity=ElasticSearchActivities.create_index,
                args=(
                    video,
                    subtitles,
                ),
                start_to_close_timeout=timedelta(minutes=1),
            )

        return {
            "status": "completed",
            "processed_videos": len(videos),
        }


async def run_workflow():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        PodcastTranscriptWorkflow,
        args=(data,),
        id="podcast_transcript_workflow",
        task_queue="podcast_transcript_task_queue",
    )

    print("Workflow completed! Result:", result)


if __name__ == "__main__":
    asyncio.run(run_workflow())
