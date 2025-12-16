import time
import asyncio
import sys
from processing_engine.utils.llm_client import LLMClient
from processing_engine.utils.prompts import markdown_messages
from processing_engine.utils.doc_utils import fetch_file, stream_to_images, to_base64 

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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m processor.markdown <pdf_url>")
        sys.exit(1)
    pdf_url = sys.argv[1]
    asyncio.run(to_markdown(pdf_url))