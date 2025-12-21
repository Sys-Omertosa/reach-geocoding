import asyncio
import logging
import json
import sys
from processing_engine.worker import QueueWorker
from processing_engine.models.schemas import QueueJob
from utils import load_env, supabase_client

#################################################

load_env()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
supabase = supabase_client()

async def main(LIMIT = 5):
    worker = QueueWorker(supabase)

    logger.info("Initializing worker...")
    await worker.initialize()
    logger.info("Worker ready")

    while True:
        response = supabase.schema("pgmq_public").rpc("read", {
            "queue_name": "processing_queue",
            "sleep_seconds": 60,
            "n": LIMIT
        }).execute()
        print(f"Jobs fetched: {len(response.data)}")
        print(json.dumps(response.data, indent=4, sort_keys=False))
        jobs = [QueueJob(**job) for job in response.data]
        
        if jobs:
            tasks = [worker.process_job(job) for job in jobs]
            await asyncio.gather(*tasks)
        
        if int(len(response.data)) < int(LIMIT):
            break

if __name__ == "__main__":
    limit = sys.argv[1]
    asyncio.run(main(limit))