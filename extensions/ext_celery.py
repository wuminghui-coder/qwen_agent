from celery import Celery

def init_celery(app_config: dict):
    celery_app = Celery(
        'tasks',
        broker='redis://:agent123456@localhost:6379/0',  # 使用 Redis 作为消息代理
        backend='redis://:agent123456@localhost:6379/0',   # 使用 Redis 作为结果存储
        #task_ignore_result=True,
    )
    
    app_config["celery"] = celery_app