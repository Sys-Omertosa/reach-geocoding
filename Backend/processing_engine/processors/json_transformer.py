import json
from pydantic import ValidationError
from processing_engine.processor_utils.llm_client import LLMClient
from processing_engine.models.schemas import ExtractedContent, Alert, AlertArea, StructuredAlert
from processing_engine.processor_utils.prompts import json_messages

class JSONTransformer:
    def __init__(self, llm:str):
        self.llm = LLMClient(llm)
        
    async def transform(self, extracted: ExtractedContent, document_id: str, alert_id: str) -> tuple[dict, Alert, list[AlertArea]]:
        """Transform markdown to structured JSON"""
        json_prompt = json_messages(extracted.markdown)
        extracted_json = self.llm.call(json_prompt)
        print(f"RAW JSON response from model: \n{extracted_json}")

        # Parse response
        json_response, alert, alert_areas = await self._parse(extracted_json, document_id, alert_id)

        return json_response, alert, alert_areas
        
    async def _parse(self, response: str, document_id: str, alert_id: str) -> tuple[dict, Alert, list[AlertArea]]:
        """Parse LLM JSON response"""
        response = response[response.find("{") : response.rfind("}") + 1]
        
        try:
            # Parse and validate JSON structure
            structured_alert = StructuredAlert.model_validate_json(response)
            json_response = structured_alert.model_dump()
            
            # Create Alert object
            alert_model = Alert(
                id=alert_id,
                document_id=document_id,
                category=structured_alert.category,
                event=structured_alert.event,
                urgency=structured_alert.urgency,
                severity=structured_alert.severity,
                description=structured_alert.description,
                instruction=structured_alert.instruction,
                effective_from=structured_alert.effective_from,
                effective_until=structured_alert.effective_until
            )

            alert = alert_model.model_dump(mode='json')
            
            # Create AlertArea objects from the areas list
            alert_areas = []
            for area_list in structured_alert.areas:
                place_ids = await self._geocode(area_list.place_names)
                for place_id in place_ids:                    
                    alert_area_model = AlertArea(
                        alert_id=alert_id,
                        place_id=place_id,
                        specific_effective_from=area_list.specific_effective_from,
                        specific_effective_until=area_list.specific_effective_until,
                        specific_urgency=area_list.specific_urgency,
                        specific_severity=area_list.specific_severity,
                        specific_instruction=area_list.specific_instruction
                    )
                    alert_areas.append(alert_area_model.model_dump(mode='json'))
            
            return json_response, alert, alert_areas
            
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM returned invalid JSON: {e}")
        except ValidationError as e:
            raise ValueError(f"JSON doesn't match expected schema: {e}")