
from fastapi import APIRouter
from controllers.app   import app_model
from controllers.files import file_service
from controllers.config import app_config

api_router = APIRouter()

api_router.include_router(app_model.router,     tags=["数据库接口测试"])
api_router.include_router(file_service.router,  tags=["文件上传下载服务"])
api_router.include_router(app_config.router,    tags=["配置测试接口"])


