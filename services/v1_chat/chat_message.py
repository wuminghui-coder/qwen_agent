import logging
import json
from core.user.api_token import ApiTokenServiceUpdate
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi import Depends, HTTPException, status, FastAPI, File, UploadFile, Header, Request
from core.music_agent import music_agent_services
from sqlmodel import Session, select
from typing import Union, Optional, Annotated
from fields.app_fields import ChatMessage
from fields.app_fields import ResponesMessage
from extensions.exten_sql import CustomJSONResponse
from fields.v1_version import V1ResponesMessage
from fastapi.responses import JSONResponse
from core.util import measure_time
logger = logging.getLogger(__name__)

v1_chat_router = APIRouter()

@v1_chat_router.post("/v1/chat-messages")
async def chat_v1_messages(user_query: ChatMessage, request_db: Request):
    answer = await music_agent_services(session=request_db.state.db, 
                                    user_name=user_query.user, 
                                    user_query=user_query.query, 
                                    conversation_id=user_query.conversation_id)
    
    respones = V1ResponesMessage()
    respones.copy_from_v2_respones(answer)
    
    logger.debug(respones.json())

    answer_string = json.dumps({
        "answer": respones.json(exclude_none=True),
        "event": "message"
    })
    
    return StreamingResponse("data: " + answer_string, media_type="text/event-stream")


@v1_chat_router.post("/v3/chat-messages", response_model=V1ResponesMessage, response_class=CustomJSONResponse)
async def chat_v3_messages(user_query: ChatMessage, request_db: Request, authorization: Annotated[str, Header()]):
    app_id = ApiTokenServiceUpdate.verify_token(request_db.state.db, authorization)
    if not app_id:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    answer = await music_agent_services(session=request_db.state.db, 
                                    user_name=user_query.user, 
                                    user_query=user_query.query, 
                                    conversation_id=user_query.conversation_id)
    
    respones = V1ResponesMessage()
    respones.copy_from_v2_respones(answer)

    return JSONResponse(content=respones.dict(exclude_none=True))





