import asyncio
from utils import supabase_client
from processing_engine.processors.document_processor import DocumentProcessor
from processing_engine.processors.json_transformer import Transformer
from processing_engine.models.schemas import QueueJob, AlertData, AlertArea
import logging

class QueueWorker:
    def __init__(self, supabase):
        self.logger = logging.getLogger(__name__)
        self.db = supabase
        self.doc_processor = DocumentProcessor("ernie-4.5-vl:baidu")
        self.alert_processor = Transformer("ernie-x1:baidu")
    
    async def process_job(self, job: QueueJob):
        try:
            self.logger.info(f"Processing {job.msg_id}")
            extracted = await self.doc_processor.extract(job)
            alert, alert_areas = await self.alert_processor.transform(extracted)
            await self._upsert(alert, alert_areas)
            await self._mark_complete(job.msg_id)
            return True
        except Exception as e:
            self.logger.error(f"Job {job.msg_id} failed: {e}")
            await self._mark_failed(job.msg_id, str(e))
            return False
        
    async def upsert(self, alert: AlertData, alert_areas: AlertArea):
        """Upsert new alerts to table"""

        # Upsert the single alert row
        self.db.table("alerts").upsert(alert, on_conflict='document_id').execute()

        #Unpack and upsert the alerts

