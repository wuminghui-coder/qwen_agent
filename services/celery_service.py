from tasks.task_test import clean_document_task
from fastapi import APIRouter
from celery.result import AsyncResult

celery_router = APIRouter()

@celery_router.post("/add/")
async def create_task():
    task = clean_document_task.delay()  # 调用 Celery 任务
    return {"task_id": task.id}

@celery_router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }