from fastapi.responses import FileResponse
import os
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi import FastAPI, Depends, HTTPException, status
from core.music_agent import MusicAgent
from core.util import is_valid_uuid, upload_lyric_file
from fastapi import APIRouter
from fields.app_fields import ResponesMessage
from extensions.exten_sql import CustomJSONResponse
from fastapi import Depends, HTTPException, status, FastAPI, File, UploadFile, Header, Request
from core.user.music_data import MusicServiceUpdate
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import logging
from core.api_service import audio_api
from fields.audio_fields import VoiceType
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

audio_router= APIRouter()

@audio_router.get("/audio")
async def stream_audio(query:str, request_db: Request):
    callback, synthesizer = audio_api.get_audio_service(VoiceType.longcheng.value)
    synthesizer.call(query)
    return StreamingResponse(callback.stream_audio(), media_type="audio/mpeg")

async def generate_html_response(file_path:str):
    with open(file_path, 'r', encoding='utf-8') as file:
        return HTMLResponse(content=file.read(), status_code=200)
    
@audio_router.get("/audio/index", response_class=HTMLResponse)
async def read_items():
    return await generate_html_response('templates/audio.html')

@audio_router.post("/saudio")
async def receive_audio(request: Request):
    audio_chunks = []
    
    async for chunk in request.stream():
        audio_chunks.append(chunk)

    # 在这里处理音频数据（例如，保存或转码）
    audio_data = b''.join(audio_chunks)

    # 假设你会在这里进行音频处理
    # ...

    return JSONResponse(content={"message": "音频接收成功"})