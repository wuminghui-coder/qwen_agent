
import uuid
from typing import Any, List, Optional
import random
import string
import time
import logging
import os

logger = logging.getLogger(__name__)

def generate_random_id(length=10):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def is_valid_uuid(uuid_string: str) -> bool:
    try:
        # 尝试创建一个 UUID 对象
        uuid_obj = uuid.UUID(uuid_string)
        return str(uuid_obj) == uuid_string  # 确保格式相同
    except ValueError:
        return False  # 如果抛出异常，则不是有效的 UUID

async def measure_time():
    start_time = time.time()
    yield
    process_time = time.time() - start_time
    logger.debug(f"请求总耗时： {process_time} seconds")

UPLOAD_DIR = "storage/files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def upload_lyric_file(lyric:Optional[str] = None)->Optional[str]:
    if not lyric:
        return None
    
    file_id = str(uuid.uuid4())  # 生成唯一的文件 ID
    file_location = os.path.join(UPLOAD_DIR, file_id)
    
    with open(file_location, "w") as f:
        f.write(lyric)

    return "http://172.30.13.160:5001/file/lyric/" + file_id