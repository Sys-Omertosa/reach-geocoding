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
from processing_engine.models.schemas import QueueJob, ExtractedContent,Alert, AlertArea, StructuredAlert

