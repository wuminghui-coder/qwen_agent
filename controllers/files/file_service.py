
from fastapi.responses import StreamingResponse
import asyncio
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import uuid
from fastapi import APIRouter

router = APIRouter()

UPLOAD_DIR = "storage/files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

files_db = {}

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())  # 生成唯一的文件 ID
    file_location = os.path.join(UPLOAD_DIR, file_id)
    
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    files_db[file_id] = file.filename  # 存储文件 ID 和原始文件名的映射
    return {"file_id": file_id, "filename": file.filename}

@router.get("/download/{file_id}")
async def download_file(file_id: str):
    if file_id in files_db:
        original_filename = files_db[file_id]
        file_path = os.path.join("storage/files", file_id)
        
        return FileResponse(file_path, media_type='application/octet-stream', filename=original_filename)
    else:
        raise HTTPException(status_code=404, detail="文件未找到")
    


