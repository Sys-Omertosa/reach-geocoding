import json
from processing_engine.processor_utils.llm_client import LLMClient
from processing_engine.models.schemas import ExtractedContent, Alert, AlertArea, StructuredAlert
from processing_engine.processor_utils.prompts import json_messages
from uuid import uuid4
#from geocoding import geocoder

class Transformer:
    def __init__(self, llm:str):
        self.llm = LLMClient(llm)
        
    async def transform(self, extracted: ExtractedContent) -> Alert:
        """Transform markdown to structured JSON"""
        json_prompt = json_messages(extracted.markdown)
        extracted_json = self.llm.call(json_prompt)   

        # Parse response
        alert, alert_areas = self._parse(extracted_json)

        return Alert(**alert), [AlertArea(**alert_areas)]
        
    def _parse(self, response: str) -> dict:
        """Safely parse LLM JSON response"""
        response = response[response.find("{") : response.rfind("}") + 1]
        json_response = StructuredAlert(**response)



        
        try:
            return json.loads(json_response)
        except json.JSONDecodeError as e:
            # Log the error and attempt recovery
            raise ValueError(f"LLM returned invalid JSON: {e}")