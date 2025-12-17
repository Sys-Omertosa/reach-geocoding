import json
from processing_engine.processor_utils.llm_client import LLMClient
from processing_engine.models.schemas import ExtractedContent, Alert, AlertArea

class Transformer:
    def __init__(self, llm:str):
        self.llm = LLMClient(llm)
        
    async def transform(self, extracted: ExtractedContent) -> Alert:
        """Transform markdown to structured JSON"""
        
        # Build a focused prompt
        prompt = self._build_extraction_prompt(extracted.markdown)
        
        message = self.anthropic.messages.create(
            model="claude-sonnet-4-20250514",  # Good balance of speed/quality
            max_tokens=2048,
            temperature=0,  # Deterministic output
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Parse response
        response_text = message.content[0].text
        alert_data = self._parse_llm_response(response_text)
        
        # Add job metadata
        alert_data["job_id"] = extracted.job_id
        
        return Alert(**alert_data)
    
    def _build_extraction_prompt(self, markdown: str) -> str:
        """Create prompt that minimizes repetition"""
        
        return f"""Extract disaster alert information from this text and return ONLY a JSON object with these fields:

{{
  "event_type": "type of disaster (flood, earthquake, fire, etc.)",
  "severity": "severity level (extreme, severe, moderate, minor)",
  "areas_affected": ["list", "of", "affected", "areas"],
  "issued_at": "ISO 8601 datetime when alert was issued",
  "expires_at": "ISO 8601 datetime when alert expires (or null)",
  "description": "concise summary of the situation",
  "instructions": "what people should do (or null)",
  "source_agency": "issuing organization"
}}

Text to analyze:
{markdown}

Return ONLY the JSON object, no markdown formatting or explanation."""
    
    def _parse_llm_response(self, response: str) -> dict:
        """Safely parse LLM JSON response"""
        
        # Remove markdown code blocks if present
        response = response.strip()
        if response.startswith("```"):
            response = response.split("```")[1]
            if response.startswith("json"):
                response = response[4:]
        
        response = response.strip()
        
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            # Log the error and attempt recovery
            raise ValueError(f"LLM returned invalid JSON: {e}")