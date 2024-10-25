
import logging
from fastapi import FastAPI, Request, Depends, HTTPException
from services.chat_message import chat_router
from services.stream_service import stream_router
from services.celery_service import celery_router
from controllers import api_router
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from config.app_config import settings
import uvicorn

from extensions.exten_api import init_api
from extensions.exten_agent import init_agent
from extensions.ext_sentry import init_sentry
from extensions.exten_sql import init_db, DatabaseSessionMiddleware
from extensions.exten_redis import init_redis
from extensions.ext_celery import init_celery

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

app_config = {}

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"
 
def create_app_core(app:FastAPI):
    if settings.all_cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.all_cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

def create_fastapi_app()->FastAPI:
    app = FastAPI(
        title="My Music Agent",
        description="Music Agent",
        version="1.0.0",
        generate_unique_id_function=custom_generate_unique_id,
    )
    
    #create_app_core(app)
    app.add_middleware(DatabaseSessionMiddleware) #添加中间件
    
    app.include_router(chat_router,   tags=["智能体对话"])
    app.include_router(stream_router, tags=["流式回复测试"])
    app.include_router(api_router, prefix="/console/api")
    app.include_router(celery_router, prefix="/console/api", tags=["celery异步测试"])

    init_agent(app_config)
    init_api(app_config)
    init_sentry()
    init_db()
    init_redis(app_config)
    init_celery(app_config)

    return app

app = create_fastapi_app()

celery = app_config["celery"]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)



