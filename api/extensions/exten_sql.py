
from sqlmodel import Session, create_engine, select,SQLModel, Field
from config.app_config import settings
from models.model import User
from typing import Annotated
from collections.abc import Generator
from sqlmodel import Session
from fastapi import FastAPI, Request, Depends, HTTPException, status
import logging
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time

logger = logging.getLogger(__name__)

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), pool_size=40)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
            session.commit()  # 提交事务
        except Exception:
            session.rollback()  # 回滚事务
            raise 

SessionDep = Annotated[Session, Depends(get_db)]

class DatabaseSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        with Session(engine) as session:
            request.state.db = session
            try:
                start_time = time.time()
                response = await call_next(request)
                process_time = time.time() - start_time
                logger.debug(f"请求总耗时： {process_time} seconds")
                session.commit()  # 提交事务
            except Exception:
                session.rollback()  # 回滚事务
                raise  # 重新抛出异常
            return response
        
class CustomJSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        logger.debug("Response content: %s", content)  # 打印内容
        return super().render(content)

