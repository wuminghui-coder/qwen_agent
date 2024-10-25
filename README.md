# fastapi学习
---
## 启动
```shell
    uvicorn app:app --reload
    celery -A app.celery worker -Q dataset --loglevel INFO
```
---
## 地址
- http://127.0.0.1:8000/docs



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

#db.select(App).where(*filters).order_by(App.created_at.desc()),
#apps = db.session.query(App).filter(
#                App.status == 'normal'
#            ).order_by(App.created_at.desc()).paginate(page=page, per_page=50)
#db.select(InstalledApp).join(App, InstalledApp.app_id == App.id)
#               .join(TenantAccountJoin, TenantAccountJoin.account_id == App.uuid).where(*filters).order_by(App.created_at.desc()),

#installed_apps = db.session.query(InstalledApp).join(App, InstalledApp.app_id == App.id).filter(
#            App.is_public == True,
#            InstalledApp.tenant_id == current_tenant_id
#        ).all()
#app_list = db.session.query(App).all()
#db.select(InstalledApp).join(App, InstalledApp.app_id == App.id)
# .join(TenantAccountJoin, TenantAccountJoin.account_id == App.uuid).where(*filters).order_by(App.created_at.desc()),


#from sqlmodel import select

#@app.get("/users/{user_id}")
#def read_user(user_id: int):
#    statement = select(User).where(User.id == user_id).options(selectinload(User.posts))
#    return session.exec(statement).first()
#使用 options() 进行预加载stmt = select(User).options(selectinload(User.posts)) 

#users = session.exec(select(User.email, User.name)).all()
#@app.get("/users/")
#def read_users(skip: int = 0, limit: int = Query(10)):
#    statement = select(User).offset(skip).limit(limit)
#    return session.exec(statement).all()


    #with Session(engine) as session:  
    #    user = session.exec(
    #        select(User).where(User.email == settings.FIRST_SUPERUSER)
    #    ).first()
    #    if not user:
    #        user_in = UserCreate(
    #            email=settings.FIRST_SUPERUSER,
    #            password=settings.FIRST_SUPERUSER_PASSWORD,
    #            is_superuser=True,
    #        )
    #        user = crud.create_user(session=session, user_create=user_in)




    #Field(default=None, sa_column_kwargs={"type_": "TEXT"})

    #class SettingItem(SQLModel):
    #    key: str
    #    value: Any  # 使用 Any 以支持不同类型的值
    #message_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    #conversation_id: uuid.UUID = Field(foreign_key='conversations.id')
    #conversation: Conversation = Relationship(back_populates="messages")
      #items: List[str] 
    #settings: Dict[str, str]
    #settings: Dict[str, str]         = Field(sa_column=JSON)
    #settings: Dict[str, SettingItem] = Field(sa_column=JSON)
    #message_items: List["Message"] = Relationship(back_populates="owner", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


```


## celery任务队列使用

```
#@app.post("/add/")
#async def create_task(x: int, y: int):
#    task = add.delay(x, y)  # 调用 Celery 任务
#    return {"task_id": task.id}

#from celery.result import AsyncResult

#@app.get("/task/{task_id}")
#async def get_task_status(task_id: str):
#    task_result = AsyncResult(task_id, app=celery_app)
#    return {
#        "task_id": task_id,
#        "status": task_result.status,
#        "result": task_result.result
#    }

#celery -A app.celery worker -Q dataset --loglevel INFO

```


## fastapi
- 加入路由 api_router.include_router(file_service.router, prefix="/users", tags=["users"])

lower() 将关键词转换为小写。
开发阶段
uvicorn app:app --host 0.0.0.0 --port=5001 --workers 4 --reload

生成阶段
uvicorn app:app --host 0.0.0.0 --port=5001 --workers 4