import logging
from uuid import uuid4
from typing import List
import time
from datetime import datetime, timezone
#from processing_engine.processors.document_processor import DocumentProcessor
#from processing_engine.processors.json_transformer import JSONTransformer
from processing_engine.processors.pipeline_processor import PipelineProcessor
from processing_engine.models.schemas import QueueJob
from processing_engine.processor_utils.pipeline_prompts import _load_examples


class QueueWorker:
    def __init__(self, supabase):
        self.logger = logging.getLogger(__name__)
        self.db = supabase
        self.processor = PipelineProcessor("ernie-4.5-vl-thinking:baidu")
        self._cache_initialized = False

    async def initialize(self):
        """Pre-warm caches before processing jobs"""
        if not self._cache_initialized:
            self.logger.info("Pre-warming example files cache...")
            try:
                await _load_examples()
                self._cache_initialized = True
            except Exception as e:
                self.logger.error(f"Failed to pre-warm cache: {e}")
                raise

    async def process_job(self, job: QueueJob):
        try:
            if not self._cache_initialized:
                await self.initialize()

            start_time = time.time()
            document_id = job.message.document_id
            alert_id = str(uuid4())
            self.logger.info(f"Processing {job.msg_id}")

            json_response, alert, alert_areas = await self.processor.transform(job, document_id, alert_id)
            if json_response and alert and alert_areas:
                self.logger.info(f"Processed job {job.msg_id} successfully")
            end_time = time.time()
            json_response["processing_time"] = f"{end_time-start_time:.2f}"

            uploaded_success = await self._upload(json_response, alert, alert_areas)
            if uploaded_success:
                queue_pop_success = await self._mark_complete(job.msg_id)
                if queue_pop_success:
                    self.logger.info(f"Successfully uploaded job {job.msg_id}")
                    return True

            # print(f"\n\n\n Processed Dicts:")
            # print(f"\n\n\n JSON:")
            # print(json.dumps(json_response, indent=4, sort_keys=False))
            # print(f"\n\n\n Alert:")
            # print(json.dumps(alert, indent=4, sort_keys=False))
            # print(f"\n\n\n Alert_Areas:")
            # for alert_area in alert_areas:
            #     print(json.dumps(alert_area, indent=4, sort_keys=False))
        except Exception as e:
            self.logger.error(f"Job {job.msg_id} failed: {e}")
            return False

    async def _upload(self,json_response: dict, alert: dict, alert_areas: List[dict]):
        """Upsert new alerts to table"""
        try:
            document_id = alert["document_id"]
            
            # Upload the Markdown and JSON
            document_response = await self.db.table("documents").update({
                "processed_at": datetime.now(timezone.utc).isoformat(),
                "structured_text": json_response
            }).eq("id", document_id).execute()
            if document_response.error or not document_response.data:
                self.logger.error(f"Text upload failed for document {document_id}: {e}")
                raise Exception(document_response.error)
                        
            # Upsert the single alert row
            alert_response = await self.db.table("alerts").upsert(alert, on_conflict='document_id').execute()
            if alert_response.error or not alert_response.data:
                self.logger.error(f"Alert upload failed for alert {document_id}: {e}")
                raise Exception(alert_response.error)
            
            # Upsert the alert_areas rows
            alert_areas_response = await self.db.table("alert_areas").upsert(alert_areas, on_conflict='alert_id').execute()
            if alert_areas_response.error or not alert_areas_response.data:
                self.logger.error(f"Alert_Areas upload failed for document {document_id}: {e}")
                raise Exception(alert_areas_response.error)
                        
            self.logger.info(f"Successfully uploaded data for document {document_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Upload failed for document {document_id}: {e}")
            return False
    
    async def _mark_complete(self, msg_id: int):
        response = await self.db.schema("pgmq_public").rpc("delete", {
            "queue_name": "processing_queue",
            "message_id": msg_id
        }).execute()
        if response.data and not response.error:
            self.logger.info(f"Successfully removed job {msg_id} from queue")
            return True
        else:
            self.logger.error(f"Error removing job {msg_id}: {response.error}")
            return False


# class QueueWorker:
#     def __init__(self, supabase):
#         self.logger = logging.getLogger(__name__)
#         self.db = supabase
#         self.doc_processor = DocumentProcessor("ernie-4.5-vl:baidu")
#         self.alert_processor = JSONTransformer("ernie-4.5-vl:baidu")

#     async def process_job(self, job: QueueJob):
#         try:
#             start_time = time.time()
#             document_id = job.message.document_id
#             alert_id = str(uuid4())
#             self.logger.info(f"Processing {job.msg_id}")

#             extracted = await self.doc_processor.extract(job)
#             markdown = extracted.markdown
#             print(markdown)

#             json_response, alert, alert_areas = await self.alert_processor.transform(extracted, document_id, alert_id)
#             end_time = time.time()
#             json_response["processing_time"] = f"{end_time-start_time:.2f}"
#             # uploaded_success = await self._upload(markdown, json_response, alert, alert_areas)
#             # if uploaded_success:
#             #     await self._mark_complete(job.msg_id)
#             print(f"\n\n\n Processed Dicts:")
#             print(f"\n\n\n JSON:")
#             print(json.dumps(json_response, indent=4, sort_keys=False))
#             print(f"\n\n\n Alert:")
#             print(json.dumps(alert, indent=4, sort_keys=False))
#             print(f"\n\n\n Alert_Areas:")
#             for alert_area in alert_areas:
#                 print(json.dumps(alert_area, indent=4, sort_keys=False))
#             return True
#         except Exception as e:
#             self.logger.error(f"Job {job.msg_id} failed: {e}")
#             return False

#     async def _upload(self, markdown: str, json_response: dict, alert: dict, alert_areas: List[dict]):
#         """Upsert new alerts to table"""
#         try:
#             document_id = alert["document_id"]
            
#             # Upload the Markdown and JSON
#             document_response = self.db.table("documents").update({
#                 "processed_at": datetime.now(timezone.utc).isoformat(),
#                 "raw_text": markdown,
#                 "structured_text": json_response
#             }).eq("id", document_id).execute()
#             if document_response.error or not document_response.data:
#                 self.logger.error(f"Text upload failed for document {document_id}: {e}")
#                 raise Exception(document_response.error)
                        
#             # Upsert the single alert row
#             alert_response = self.db.table("alerts").upsert(alert, on_conflict='document_id').execute()
#             if alert_response.error or not alert_response.data:
#                 self.logger.error(f"Alert upload failed for alert {document_id}: {e}")
#                 raise Exception(alert_response.error)
            
#             # Upsert the alert_areas rows
#             alert_areas_response = self.db.table("alert_areas").upsert(alert_areas, on_conflict='alert_id').execute()
#             if alert_areas_response.error or not alert_areas_response.data:
#                 self.logger.error(f"Alert_Areas upload failed for document {document_id}: {e}")
#                 raise Exception(alert_areas_response.error)
                        
#             self.logger.info(f"Successfully uploaded data for document {document_id}")
#             return True
            
#         except Exception as e:
#             self.logger.error(f"Upload failed for document {document_id}: {e}")
#             return False
    
#     async def _mark_complete(self, msg_id: int):
#         response = self.db.schema("pgmq_public").rpc("delete", {
#             "queue_name": "processing_queue",
#             "message_id": msg_id
#         }).execute()
#         if not response.error:
#             self.logger.info(f"Successfully removed job {msg_id} from queue")
#         else:
#             self.logger.error(f"Error removing job {msg_id}: {response.error}")