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

song_router= APIRouter()

@song_router.get("/file/lyric/{file_id}", response_class=HTMLResponse)
async def get_lyric(file_id:str):
    file_path = os.path.join("storage/files", file_id)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/octet-stream', filename= file_id + ".lrc")
    else:
        raise HTTPException(status_code=404, detail="文件未找到")
    

@song_router.get("/song/{song_id}", response_model=ResponesMessage, response_class=CustomJSONResponse)
async def get_song_url(song_id: str, request_db: Request):
    music = MusicAgent(session=request_db.state.db, conversation_id="", user="")
    answer = await music.play_id_music(song_id)
    if not answer:
        return {"type": -1, "message": "获取歌曲失败"}
    
    if answer.slots:
        answer.slots[0].lyric = upload_lyric_file(answer.slots[0].lyric)
    return answer

@song_router.get("/music/song_id/{music_id}")
async def get_musci_data(music_id: str, request_db: Request):
    music_id = music_id.replace(".mp3","").replace(".flac","")
    music_info = MusicServiceUpdate.get_music_by_id(session=request_db.state.db, 
                                                    music_id=music_id)
    if not music_info:
        return {"type": -1, "message": "获取歌曲失败"}
    
    audio = MusicServiceUpdate.get_audio_by_music_id(session=request_db.state.db, 
                                             music_id=music_info.id)
    if not audio:
        return {"type": -1, "message": "获取歌曲失败"}
    return Response(audio.data, media_type="application/octet-stream")

@song_router.get("/music/lyric/{music_id}")
async def get_musci_lyric(music_id: str, request_db: Request):
    music_id = music_id.replace(".lrc","")
    music_info = MusicServiceUpdate.get_music_by_id(session=request_db.state.db, 
                                                    music_id=music_id)
    if not music_info:
        return {"type": -1, "message": "获取歌曲失败"}
    
    return Response(music_info.lyric, media_type="application/octet-stream")