from fastapi import FastAPI, Request
from fastapi import APIRouter
from core import crud
from extensions.exten_sql import SessionDep

router = APIRouter()

@router.get("/config/{email}")
def get_login(email:str, session: SessionDep):

    user = crud.create_user(session=session, user_name=email)

    return user

@router.get("/config/{email}")
async def read_user(email:str, request: Request):
    session = request.state.db  # 获取数据库会话
    user = crud.create_user(session=session, user_name=email)
    return user
