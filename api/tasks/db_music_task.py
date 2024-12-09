from celery import Celery
from celery import shared_task
from celery.result import AsyncResult
from core.user.music_data import MusicServiceUpdate
from fields.app_fields import MusicMessage
from sqlmodel import Session, select
import logging
from extensions.exten_sql import engine

logger = logging.getLogger(__name__)

#@shared_task(queue='clean', bind=True, soft_time_limit=300, time_limit=360)
@shared_task(queue="dataset", soft_time_limit=300, time_limit=360)
def creat_db_music_task(music_info: dict):
    with Session(engine) as session:
        music_resp = MusicServiceUpdate.create_db_music(session=session, 
                                                        music_info=MusicMessage.parse_obj(music_info))
        if not music_resp:
            logger.error("create music db error")
        logger.debug(f"create music {music_resp.song_name}, {music_resp.song_id}")
