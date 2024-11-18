from celery import Celery
from celery import shared_task
from celery.result import AsyncResult
from core.user.music_data import MusicServiceUpdate
from fields.app_fields import MusicMessage
from sqlmodel import Session, select
import logging

logger = logging.getLogger(__name__)

#@shared_task(queue='clean', bind=True, soft_time_limit=300, time_limit=360)
@shared_task(queue="dataset", soft_time_limit=300, time_limit=360)
def add_memory_task(memory: str, user_id: str):
    from extensions.exten_mem0 import mem0_api
    resp = mem0_api.add_memories(memory=memory, 
                                user_id=user_id)
    logger.debug(f"add memory {memory} to user {user_id}, result {resp}")
