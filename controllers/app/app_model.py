from fastapi import FastAPI, Request
from fastapi import APIRouter
from extensions.exten_sql import SessionDep
import logging
from config.app_config import settings
from pydantic import BaseModel, Field
from core.user.user import UserServiceUpdate
from core.user.conversation import ConversationServiceUpdate

router = APIRouter()

class requestBody(BaseModel):
    name: str | None = Field(
        default= None,
        title="名字", 
        min_length=1
    )

    query:str | None = Field(
        title="用户请求的问题", 
        min_length=1
    )

    answer:str | None = Field(
        title="回复问题", 
        min_length=1
    )

    conversation_id:str |None = Field(
        default= None,
        title="会问ID", 
        min_length=1
    )

    user_id:str | None = Field(
        default= None,
        title="用户ID", 
        min_length=1
    )

    message_id:str |None = Field(
        default= None,
        title="消息ID", 
        min_length=1
    )
 
    page: int | None

    page_size:int| None

    limit: int | None

@router.post("/create_user")
async def create_user(body:requestBody, session: SessionDep):
    user = UserServiceUpdate.create_user(
        session=session, 
        user_name=body.name
    )
    return user

@router.post("/update_user")
async def update_user(body:requestBody, request: Request):
    session = request.state.db  # 获取数据库会话
    user = UserServiceUpdate.update_user(
        session=session, 
        user_id=body.user_id,
        name=body.name
    )
    return user

@router.post("/delete_user")
async def delete_user(body:requestBody, request: Request):
    session = request.state.db  # 获取数据库会话
    user = UserServiceUpdate.delete_user(
        session=session, 
        user_id=body.user_id,
    )
    return user

@router.get("/all_user")
async def all_user(request: Request):
    session = request.state.db  # 获取数据库会话
    user_list = UserServiceUpdate.get_all_user(session)
    return user_list


@router.post("/create_conversation")
async def create_conversation(body:requestBody, request: Request):
    session = request.state.db  # 获取数据库会话
    conversation = ConversationServiceUpdate.create_conversation(session, body.user_id, body.name)
    return conversation