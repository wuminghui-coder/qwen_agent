from celery import Celery
from celery import shared_task

@shared_task(queue="dataset")
def clean_document_task():
    print("Cleaning document task started")

    return {"status": "Task completed"}