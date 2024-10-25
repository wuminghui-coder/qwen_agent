from pydantic import BaseModel, Field
import logging
import time
from core.agent_service import agent_chat,play_id_music
from fastapi import APIRouter
from config.app_config import settings
from fastapi import FastAPI, Request
from core import crud
from core.prompt import MUSIC_PROMPT, CHAT_PROMPT
from fields.message_type import MessageType
from fastapi import FastAPI, Depends
import time
import json
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)
# 定义 Pydantic 模型
chat_router = APIRouter()

class ChatMessage(BaseModel):
    query:str = Field(
        title="用户请求的问题", 
        min_length=1
    )

    conversation_id:str |None = Field(
        default= None,
        title="会问ID", 
        #min_length=1
    )

    user:str = Field(
        title="用户名字", 
        min_length=1
    )

async def measure_time():
    start_time = time.time()
    yield
    process_time = time.time() - start_time
    logger.debug(f"请求总耗时： {process_time} seconds")

@chat_router.post("/v1/chat-messages", dependencies=[Depends(measure_time)])
async def chat_messages(user_query: ChatMessage, request_db: Request):
    session = request_db.state.db  # 获取数据库会话
    answer_string = "失败"
    user_db = crud.get_uset_by_name(session=session, name = user_query.user)
    if not user_db:
        user_db = crud.create_user(session=session, user_name = user_query.user)
        if not user_db:
            return StreamingResponse(answer_string, media_type="text/event-stream")
        
        conversation = crud.create_conversation(session=session, user_id=user_db.id, name=user_query.query) 
        if not conversation:
            return StreamingResponse(answer_string, media_type="text/event-stream")
    if not user_query.conversation_id:
        conversation = crud.create_conversation(session=session, user_id=user_db.id, name=user_query.query) 
        if not conversation:
            return StreamingResponse(answer_string, media_type="text/event-stream")
    else:
        if not crud.is_valid_uuid(user_query.conversation_id):
            return StreamingResponse(answer_string, media_type="text/event-stream")
            
        conversation = crud.get_conversation(session=session, conversation_id=user_query.conversation_id)
        if not conversation:
            return StreamingResponse(answer_string, media_type="text/event-stream")


    answer = await agent_chat(session=session, 
                        conversation_id=conversation.id, 
                        query=user_query.query)
  
    answer["conversation_id"] = str(conversation.id)
    answer["user"]            = user_db.name
    logger.debug(answer)
    resp = {
        "answer": json.dumps(answer),
        "conversation_id": str(conversation.id),
        "event": "message"
    }

    answer_string = json.dumps(resp)

    async def async_data_generator():
        yield "data: " + answer_string
    
    return StreamingResponse(async_data_generator(), media_type="text/event-stream")


@chat_router.get("/song/{song_id}", dependencies=[Depends(measure_time)])
async def get_song_url(song_id: str):
    resp = await play_id_music(song_id)
    if not resp:
        return {"type": -1, "message": "获取歌曲失败"}
    
    return resp

@chat_router.post("/v2/chat-messages", dependencies=[Depends(measure_time)])
async def chat_v2_messages(user_query: ChatMessage, request_db: Request):
    session = request_db.state.db  # 获取数据库会话
    user_db = crud.get_uset_by_name(session=session, name = user_query.user)
    if not user_db:
        user_db = crud.create_user(session=session, user_name = user_query.user)
        if not user_db:
            return {"type": -1, "message": "创建用户失败"}
        
        conversation = crud.create_conversation(session=session, user_id=user_db.id, name=user_query.query) 
        if not conversation:
            return {"type": -1, "message": "创建会问失败"}
    
    if not user_query.conversation_id:
        conversation = crud.create_conversation(session=session, user_id=user_db.id, name=user_query.query) 
        if not conversation:         
            return {"type": -1, "message": "创建会问失败"}
    else:
        if not crud.is_valid_uuid(user_query.conversation_id):          
            return {"type": -1, "message": "会话ID不合法"}
        
        conversation = crud.get_conversation(session=session, conversation_id=user_query.conversation_id)
        if not conversation:
            return {"type": -1, "message": "获取会话失败"}


    answer = await agent_chat(session=session, 
                        conversation_id=conversation.id, 
                        query=user_query.query)
  
    answer["conversation_id"] = str(conversation.id)
    answer["user"]            = user_db.name
    logger.debug(answer)
    return answer