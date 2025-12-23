import asyncio
import modal
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os

#################################################
# IMAGE & APP SETUP
#################################################

image = (
    modal.Image.debian_slim()
    .pip_install(
        "fastapi[standard]",
        "uvicorn",
        "httpx",
        "supabase",
        "python-dotenv",
        "beautifulsoup4",
        "pandas",
        "openai",
        "PyMuPDF",
        "pillow"
    )
    .add_local_python_source("processing_engine")  # Include local dependencies
)

app = modal.App(name="reach-processor", image=image)

#################################################
# AUTH & MODELS
#################################################

auth_scheme = HTTPBearer()

class ProcessRequest(BaseModel):
    limit: int = 10

class ProcessResponse(BaseModel):
    status: str
    message: str
    job_count: int

#################################################
# BACKGROUND WORKER FUNCTION
#################################################

@app.function(
    cpu=1.0,
    memory=1024,
    secrets=[modal.Secret.from_name("reach-secrets")]
)
async def process_jobs(limit: int):
    """
    Background worker that processes jobs from the queue.
    """
    import logging
    from processing_engine.worker import QueueWorker
    from processing_engine.models.schemas import QueueJob
    from utils import load_env, async_supabase_client

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Initialize environment and clients
    load_env()
    logger.info("Initializing worker...")
    
    supabase = await async_supabase_client()
    worker = QueueWorker(supabase)
    await worker.initialize()
    logger.info("Worker ready")

    # Process jobs in batches
    total_processed = 0
    
    while True:
        try:
            # Fetch jobs from queue
            response = await supabase.schema("pgmq_public").rpc("read", {
                "queue_name": "processing_queue",
                "sleep_seconds": 300,
                "n": limit
            }).execute()
            
            jobs_data = response.data
            logger.info(f"Fetched {len(jobs_data)} jobs from queue")
            
            if not jobs_data:
                logger.info("No more jobs in queue")
                break
            
            # Parse and process jobs concurrently
            jobs = [QueueJob(**job) for job in jobs_data]
            tasks = [worker.process_job(job) for job in jobs]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Log any errors
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Job {jobs[i].id} failed: {result}")
                else:
                    total_processed += 1
            
            # Break if we got fewer jobs than requested (queue is empty)
            if len(jobs_data) < limit:
                logger.info("Reached end of queue")
                break
                
        except Exception as e:
            logger.error(f"Error processing batch: {e}", exc_info=True)
            break
    
    logger.info(f"Worker completed. Total jobs processed: {total_processed}")
    return total_processed

#################################################
# WEB ENDPOINT (Authentication & Job Spawning)
#################################################

@app.function(
    cpu=0.25,
    memory=256,
    secrets=[modal.Secret.from_name("reach-secrets")]
)
@modal.fastapi_endpoint(method="POST")
async def trigger_processing(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: ProcessRequest = ProcessRequest()
) -> ProcessResponse:
    """
    FastAPI endpoint that authenticates requests and spawns background jobs.
    Returns immediately without waiting for job completion.
    """
    # Validate authentication
    if token.credentials != os.environ.get("SECRET_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Spawn background worker (non-blocking)
    call = process_jobs.spawn(limit=request.limit)
    
    return ProcessResponse(
        status="accepted",
        message=f"Processing job spawned with ID: {call.object_id}",
        job_count=request.limit
    )

#################################################
# OPTIONAL: Status Check Endpoint
#################################################

@app.function()
@modal.fastapi_endpoint(method="GET")
async def health() -> dict:
    """Health check endpoint"""
    return {"status": "healthy", "service": "reach-processor"}