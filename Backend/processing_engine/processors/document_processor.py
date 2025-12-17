import time
import asyncio
import sys
import base64
from PIL import Image 
from typing import List

from processing_engine.processor_utils.llm_client import LLMClient
from processing_engine.processor_utils.prompts import markdown_messages
from processing_engine.processor_utils.doc_utils import fetch_file, pdf_to_images, to_base64
from processing_engine.models.schemas import QueueJob, AlertData, AlertArea, ExtractedContent

"""
async def to_markdown(url: str) -> str:
    start = time.time()
    file = await fetch_file(url)
    images = stream_to_images(file)
    llm = LLMClient("ernie-4.5-vl:baidu")
    markdown_parts = []
    for i, image in enumerate(images):
        base64_image = to_base64(image)
        messages = markdown_messages(base64_image)
        markdown = llm.call(messages)
        markdown_parts.append(f"<!-- Page {i + 1} -->\n{markdown}\n\n")
    
    end = time.time()
    time_taken = f"{end-start: .2f}s"
    final_markdown = "".join(markdown_parts)
    print(time_taken)
    print(final_markdown)
    return {
        "markdown": final_markdown,
        "time": time_taken
    }
"""

class DocumentProcessor:
    def __init__(self, llm:str):
        self.llm = LLMClient(llm)
        
    async def extract(self, job: QueueJob) -> ExtractedContent:
        """Extract markdown from various input types"""
        
        if job.message.filetype == "txt":
            # Plain text - pass through
            return ExtractedContent(
                job_id=job.message.id,
                markdown=job.message.raw_content,
                extraction_method="direct"
            )
        else:
            # Document - convert to image and use VLM
            images = await self._prepare_images(job)
            markdown = await self._extract_with_vlm(images)
            
            return ExtractedContent(
                job_id=job.msg_id,
                markdown=markdown,
                extraction_method="vlm"
            )
    
    async def _prepare_images(self, job: QueueJob):
        """Convert document to images (base64)""" 
        file = await fetch_file(job.message.url)
        if job.message.filetype in ["gif", "png"]:
            pil_image = Image.open(file)
            return to_base64(pil_image)
        
        elif job.message.filetype == "pdf":
            pil_images = pdf_to_images(file)
            return to_base64(pil_images)
            
    async def _extract_with_vlm(self, images: List[base64.b64encode]) -> str:
        markdown_parts = []
        for i, image in enumerate(images):
            messages = markdown_messages(image)
            markdown = self.llm.call(messages)
            markdown_parts.append(f"<!-- Page {i + 1} -->\n{markdown}\n\n")
        
        return "".join(markdown_parts)
"""
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m processor.markdown <pdf_url>")
        sys.exit(1)
    pdf_url = sys.argv[1]
    asyncio.run(to_markdown(pdf_url))
"""