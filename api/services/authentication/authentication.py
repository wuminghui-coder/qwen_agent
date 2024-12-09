
from fastapi import FastAPI, Depends, HTTPException, status
from core.user.app import AppServiceUpdate
from fastapi import FastAPI, Request
from fields.app_fields import CreateUser
from core.user.api_token import ApiTokenServiceUpdate
from fastapi import APIRouter

authentication = APIRouter()

@authentication.get("/agnet/{agnet_id}")
async def get_song_url(agnet_id: str, request_db: Request):
    app = AppServiceUpdate.get_app_by_id(session=request_db.state.db, 
                                         app_id=agnet_id)
    if not app:
        return {"type": -1, "message": "没有该app"}
    return app


@authentication.post("/create_app")
async def create_user(user: CreateUser, request_db: Request):
    app = AppServiceUpdate.create_app(session=request_db.state.db,
                                      app_name=user.name,
                                      describe=user.describe,
                                      version=user.version,
                                      icon=user.icon,
                                      url=user.url)
    
    if not app:
        return {"type": -1, "message": "创建应用失败"}
    
    return app

@authentication.get("/get_all_app")
async def create_user(request_db: Request):
    app_list = AppServiceUpdate.get_all_user(session=request_db.state.db)
    if not app_list:
        return {"type": -1, "message": "获取全部应用失败"}
    
    return app_list

@authentication.post("/create_token")
async def create_token(app_id: str, request_db: Request):
    token = ApiTokenServiceUpdate.create_api_token(session=request_db.state.db,
                                            app_id=app_id)
    
    if not token:
        return {"type": -1, "message": "创建token失败"}
    
    return token

@authentication.get("/get_app_token")
async def get_app_token(app_id: str, request_db: Request):
    token_list = ApiTokenServiceUpdate.get_all_app_token(session=request_db.state.db,
                                            app_id=app_id)
    
    if not token_list:
        return {"type": -1, "message": "获取所有token失败"}
    
    return token_list