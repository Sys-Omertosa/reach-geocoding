import io
import base64
from PIL import Image
import fitz
from httpx import AsyncClient

async def fetch_file(url: str):
    async with AsyncClient(timeout=60.0) as http_client:
        response = await http_client.get(url)
        response.raise_for_status()
        return response.content

def pdf_to_images(file: bytes, dpi: int = 72):
    """
    Returns a list of PIL images for a pdf file byte stream
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
    img.save(buffered, format="JPEG", quality=90)
    return base64.b64encode(buffered.getvalue()).decode()