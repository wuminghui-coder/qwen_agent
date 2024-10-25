
from core.agent_service import agent_chat
from fastapi import FastAPI,BackgroundTasks
from fastapi.responses import StreamingResponse
import asyncio
from fastapi import APIRouter

stream_router = APIRouter()
async def async_data_generator():
    for i in range(10):
        yield f"Data chunk {i}\n"
        await asyncio.sleep(1)  # 模拟异步数据生成的延迟

@stream_router.get("/async-stream")
async def stream_data():
    return StreamingResponse(async_data_generator(), media_type="text/event-stream")
