import io
import base64
from PIL import Image
import fitz
from httpx import AsyncClient
from processor.llm.llm_client import LLMClient
import time
import asyncio
import sys

def md_messages(base64_image):
    return [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract all text from this image in markdown format. Preserve the structure, headings, lists, tables, diagrams and formatting as much as possible. Return only the English markdown without any preamble."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]

async def fetch_file(url: str):
    async with AsyncClient(timeout=60.0) as http_client:
        response = await http_client.get(url)
        response.raise_for_status()
        return response.content

def to_images(file: bytes, dpi: int = 200):
    """
    Returns a list of PIL images for a file
    """
    images = []
    document = fitz.open(stream=file, filetype="pdf")

    for page_num in range(document.page_count):
        page = document[page_num]
        mat = fitz.Matrix(dpi/72, dpi/72)
        pixels = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pixels.width, pixels.height], pixels.samples)
        images.append(img)

    document.close()
    return images

def to_base64(img: Image.Image) -> str:
    """Convert PIL Image to base64 string."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

async def to_markdown(url: str) -> str:
    start = time.time()
    file = await fetch_file(url)
    images = to_images(file)
    llm = LLMClient("ernie-4.5-vl")
    markdown_parts = []

    print(f"Processing: {url}")
    for i, image in enumerate(images):
        print(f"Processing page {i+1}")

        base64_image = to_base64(image)
        messages = md_messages(base64_image)
        markdown = llm.call(messages)
        markdown_parts.append(f"<!-- Page {i + 1} -->{markdown}\n\n")
    
    end = time.time()
    time_taken = f"{end-start: .2f}s"
    final_markdown = "".join(markdown_parts)
    print(time_taken)
    print(final_markdown)
    return {
        "markdown": final_markdown,
        "time": time_taken
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m processor.markdown <pdf_url>")
        sys.exit(1)
    pdf_url = sys.argv[1]
    asyncio.run(to_markdown(pdf_url))