import logging
import json
from core.util import is_valid_uuid, upload_lyric_file

from core.user.api_token import ApiTokenServiceUpdate
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi import Depends, HTTPException, status, FastAPI, File, UploadFile, Header, Request
from sqlmodel import Session, select
from typing import Union, Optional, Annotated
from fields.app_fields import ChatMessage
from core.music_agent import music_agent_services
from fields.app_fields import ResponesMessage
from extensions.exten_sql import CustomJSONResponse
from core.util import measure_time
logger = logging.getLogger(__name__)

v2_chat_router = APIRouter()

@v2_chat_router.post("/v2/chat-messages")
async def chat_v2_messages(user_query: ChatMessage, request_db: Request):
    answer = await music_agent_services(session=request_db.state.db, 
                                    user_name=user_query.user, 
                                    user_query=user_query.query, 
                                    conversation_id=user_query.conversation_id)
    if answer.slots:
        answer.slots[0].lyric = upload_lyric_file(answer.slots[0].lyric)

    logger.debug(answer.json())

    answer_string = json.dumps({
        "answer": answer.json(),
        "event": "message"
    })
    return StreamingResponse("data: " + answer_string, media_type="text/event-stream")

@v2_chat_router.post("/v4/chat-messages", response_model=ResponesMessage, response_class=CustomJSONResponse)
async def chat_v4_messages(user_query: ChatMessage, request_db: Request, authorization: Annotated[str, Header()]):
    app_id = ApiTokenServiceUpdate.verify_token(request_db.state.db, authorization)
    if not app_id:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    
    answer = await music_agent_services(session=request_db.state.db, 
                                    user_name=user_query.user, 
                                    user_query=user_query.query, 
                                    conversation_id=user_query.conversation_id)
    if answer.slots:
        answer.slots[0].lyric = upload_lyric_file(answer.slots[0].lyric)
    return answer






