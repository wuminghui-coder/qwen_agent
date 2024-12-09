from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class VoiceType(str, Enum):
    longwan= "longwan"
    longcheng="longcheng"
    longhua = "longhua"
    longxiaoxia = "longxiaoxia"
    longxiaocheng = "longxiaocheng"
    longxiaobai = "longxiaobai"
    longlaotie = "longlaotie"
    longshu = "longshu"
    longshuo = "longshuo"
    longjing = "longjing "
    longmiao = "longmiao"
    longyue = "longyue"
    longyuan = "longyuan"
    longfei = "longfei"
    longjielidou = "longjielidou"
    longtong = "longtong"
    longxiang = "longxiang"
    loongstella = "loongstella"
    loongbella = "loongbella"
    longxiaochun= "longxiaochun"

class AudioMessage(BaseModel):
    text: Optional[str] = Field(default=None, description="")
    sentence_end:Optional[bool] = Field(default=False, description="")
   