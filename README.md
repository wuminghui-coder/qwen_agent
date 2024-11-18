# fastapi学习
---
## 启动
```shell
##python环境配置
pyenv install 3.10
pyenv global 3.10
##项目环境配置
cp .env.example .env
##启动
poetry env use 3.10
poetry install
poetry shell
```
---
## 开发阶段
- uvicorn app:app --host 0.0.0.0 --port=5001 --workers 4 --reload --log-level debug

## 生产阶段
- uvicorn app:app --host 0.0.0.0 --port=5001 --workers 4 --log-level debug

## 异步队列启动
- celery -A app.celery worker -Q dataset --loglevel INFO
---
## API文档
- http://127.0.0.1:8000/docs

## 前端地址
- http://172.30.13.160:5001/v1/index
---
## SQL数据操作
- 生成迁移文件：alembic revision --autogenerate -m "Create music table"
- 升级到数据库：alembic upgrade head
- 升级到指定版本：alembic upgrade <revision>
- 查看迁移特定版本细节: alembic show <revision>
- 列出所有迁移：alembic history
- 初始化 Alembic：alembic init alembic
- 回滚迁移：alembic downgrade -1
- 查看当前版本：alembic current
- alembic --help

## redis能力
```python
import redis
import expire

redis.close()
redis.set(key, value)
redis.get(key)

#会话存储示例
redis.set(session_id, user_data.json())
session_data = await redis.get(session_id)

#消息队列示例 
redis.publish(channel, message)
pubsub = redis.pubsub()
pubsub.subscribe(channel)

class Item(BaseModel):
    key: str
    value: str
    expire: Optional[int] = None  # 可选的过期时间（秒）

#设置缓存
@app.post("/cache/")
async def set_cache(item: Item):
    await redis.set(item.key, item.value, ex=item.expire)  # 设置过期时间
    return {"message": "Cached successfully"}

cache = redis.Redis(host='localhost', port=6379)

@app.get("/users/{user_id}")
def read_user(user_id: int):
    cached_user = cache.get(f"user:{user_id}")
    if cached_user:
        return cached_user
    # 否则从数据库中查询
```


## SQL数据库操作
```
from sqlmodel import select

select(表名) 方法
where(*filters) 过滤器list
order_by(App.created_at.desc()) 降序排序
paginate()
join() 跨表连接(需要链接的表，链接的条件字段InstalledApp.app_id == App.id)
query(表名)
filter(过滤器)
all()

options() 预加载关联的关系表提高速度 .options(selectinload(User.posts)) 

limit(限制数量)
offset(偏移)


# 使用 Any 以支持不同类型的值
Field(sa_column=JSON)
settings: Dict[str, SettingItem] = Field(sa_column=JSON)
```

---
## celery任务队列使用
```
celery -A app.celery worker -Q dataset --loglevel INFO
```

```
from celery.result import AsyncResult

task = add.delay(x, y)
return {"task_id": task.id}


@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }
```

---
## python学习笔记
- fastapi 加入路由 router.include_router(file_service.router, prefix="/users", tags=["users"])
- lower() 将关键词转换为小写。


## ffmpeg 
- ffmpeg -i output.mp3 -ar 16000 output1.mp3