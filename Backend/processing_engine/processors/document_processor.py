import time
import asyncio
import sys
import base64
from PIL import Image 
import io
from httpx import AsyncClient

from processing_engine.processor_utils.llm_client import LLMClient
from processing_engine.processor_utils.prompts import markdown_messages
from processing_engine.processor_utils.doc_utils import fetch_file, stream_to_images, to_base64
from processing_engine.models.schemas import QueueJob, AlertData, AlertArea, ExtractedContent

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

class DocumentProcessor:
    def __init__(self, llm:str):
        self.llm = LLMClient(llm)  # Uses ANTHROPIC_API_KEY env var
        
    async def extract(self, job: QueueJob) -> ExtractedContent:
        """Extract markdown from various input types"""
        
        if job.content_type == "text":
            # Plain text - pass through
            return ExtractedContent(
                job_id=job.id,
                markdown=job.raw_content,
                extraction_method="direct"
            )
        else:
            # Document - convert to image and use VLM
            image_data = await self._prepare_images(job)
            markdown = await self._extract_with_vlm(image_data)
            
            return ExtractedContent(
                job_id=job.id,
                markdown=markdown,
                extraction_method="vlm"
            )
    
    async def _prepare_images(self, job: QueueJob) -> Image:
        """Convert document to image (base64)"""
        # For PDFs, you might use pdf2image
        # For PPTX, use python-pptx or convert to PDF first
        # For images (gif, png), just encode
        
        if job.filetype in ["gif", "png"]:
            with open(job.file_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        
        elif job.filetype == "pdf":
            # Use pdf2image: images = convert_from_path(job.file_path)
            # Take first page or concatenate multiple pages
            pass
            
    async def _extract_with_vlm(self, image_base64: str) -> str:
        """Use Claude to extract markdown from image"""
        
        message = self.anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": """Extract ALL text from this disaster alert document into clean markdown format.

Preserve:
- Headings and structure
- Lists and bullet points
- Dates, times, locations
- Contact information
- Any warning or instruction text

Output only the markdown, no preamble."""
                    }
                ]
            }]
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m processor.markdown <pdf_url>")
        sys.exit(1)
    pdf_url = sys.argv[1]
    asyncio.run(to_markdown(pdf_url))