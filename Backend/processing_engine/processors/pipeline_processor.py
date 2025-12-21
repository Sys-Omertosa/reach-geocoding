import io
import time
import sys
import asyncio
import json
from uuid import uuid4
from PIL import Image 
from typing import List
from pydantic import ValidationError

from processing_engine.processor_utils.llm_client import LLMClient
from processing_engine.processor_utils.prompts import markdown_messages
from processing_engine.processor_utils.prompts import json_messages
from processing_engine.processor_utils.doc_utils import fetch_file, pdf_to_images, to_base64
from processing_engine.models.schemas import QueueJob, Alert, AlertArea, StructuredAlert

class PipelineProcessor():
    def __init__(self, llm: str):
        self.llm = LLMClient(llm)
    
    async def transform(self, job):
        lmao=1
    
    async def _prepare_images(self, job: QueueJob) -> List[bytes]:
        """Convert document to images (base64)""" 
        file = await fetch_file(str(job.message.url))
        encoded_images = []

        if job.message.filetype in ["gif", "png", "jpeg", "jpg"]:
            pil_image = Image.open(io.BytesIO(file))
            encoded_images.append(to_base64(pil_image))
        
        elif job.message.filetype == "pdf":
            pil_images = pdf_to_images(file)
            for pil_image in pil_images:
                encoded_images.append(to_base64(pil_image))
        
        return encoded_images
        