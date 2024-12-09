from aioredis import Redis, from_url

def init_redis(app_config:dict):

    redis = from_url("redis://:agent123456@localhost:6379", max_connections=10)

    app_config["redis"] = redis
