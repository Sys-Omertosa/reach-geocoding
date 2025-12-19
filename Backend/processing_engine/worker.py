import logging
from uuid import uuid4
from typing import List
import json
import time
from processing_engine.processors.document_processor import DocumentProcessor
from processing_engine.processors.json_transformer import JSONTransformer
from processing_engine.models.schemas import QueueJob

class QueueWorker:
    def __init__(self, supabase):
        self.logger = logging.getLogger(__name__)
        self.db = supabase
        self.doc_processor = DocumentProcessor("ernie-4.5-vl:baidu")
        self.alert_processor = JSONTransformer("ernie-4.5-vl:baidu")
    
    async def process_job(self, job: QueueJob):
        try:
            start_time = time.time()
            document_id = job.message.document_id
            alert_id = str(uuid4())
            self.logger.info(f"Processing {job.msg_id}")

            extracted = await self.doc_processor.extract(job)
            markdown = extracted.markdown
            print(markdown)

            json_response, alert, alert_areas = await self.alert_processor.transform(extracted, document_id, alert_id)
            end_time = time.time()
            json_response["processing_time"] = f"{end_time-start_time:.2f}"
            print(f"\n\n\n Processed Dicts:")
            print(f"\n\n\n JSON:")
            print(json.dumps(json_response, indent=4, sort_keys=False))
            print(f"\n\n\n Alert:")
            print(json.dumps(alert, indent=4, sort_keys=False))
            print(f"\n\n\n Alert_Areas:")
            for alert in alert_areas:
                print(json.dumps(alert, indent=4, sort_keys=False))
            #await self._mark_complete(job.msg_id)
            return True
        except Exception as e:
            self.logger.error(f"Job {job.msg_id} failed: {e}")
            #await self._mark_failed(job.msg_id, str(e))
            return False

    # async def _upsert(self, markdown: str, json_response: dict, alert: dict, alert_areas: List[dict]):
    #     """Upsert new alerts to table"""
    #     # Convert Pydantic models to dicts for database insertion
    #     alert = alert.model_dump()
    #     alert_areas_list = [area.model_dump() for area in alert_areas]

    #     # Upsert the single alert row
    #     self.db.table("alerts").upsert(alert, on_conflict='document_id').execute()

    #     # Upsert the alert_areas rows (a list of JSON objects)
    #     if alert_areas_list:
    #         self.db.table("alerts_areas").upsert(alert_areas_list, on_conflict='alert_id').execute()