
from fastapi import APIRouter
from services.v1_chat.chat_message import v1_chat_router
from services.v2_chat.chat_message import v2_chat_router
from services.authentication.authentication import authentication
from services.song_services.song_services import song_router
from services.audio_services.audio_services import audio_router

from services.web.agent_web import web_router

service_router = APIRouter()

service_router.include_router(v1_chat_router,     tags=["第一版本智能体"])
service_router.include_router(v2_chat_router,    tags=["第二版本智能体"])
service_router.include_router(authentication,    tags=["认证接口"])

service_router.include_router(song_router,     tags=["歌曲服务"])
service_router.include_router(web_router,     tags=["前端服务"])

service_router.include_router(audio_router,     tags=["声音服务"])