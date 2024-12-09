from pydantic import BaseModel
from pydantic import BaseModel, Field
from typing import Optional
from fields.message_type import MessageType, HistoryType

class ChatMessage(BaseModel):
    query:str = Field(
        title="用户请求的问题", 
        min_length=1
    )

    conversation_id:str |None = Field(
        default= None,
        title="会问ID", 
        #min_length=1
    )

    user:str = Field(
        title="用户名字", 
        min_length=1
    )

class CreateUser(BaseModel):
    name : str  
    describe: str  
    version: str 
    icon: str  
    url: str 

class MusicMessage(BaseModel):
    song_id: int = Field(..., description="The unique identifier for the song")
    song_name: str = Field(..., description="The name of the song")
    artist: str = Field(..., description="The artist of the song")
    lyric: Optional[str] = Field(None, description="The lyrics of the song")
    image: Optional[str] = Field(None, description="URL of the song's cover image")
    song_url: Optional[str] = Field(None, description="URL to listen to the song")


class ResponesMessage(BaseModel):
    conversation_id: str = Field(..., description="The ID of the conversation")
    user: str = Field(..., description="The user requesting the music")
    code: int = Field(default=200, description="Response code")
    type: int = Field(..., description="The genre of the song")
    message: str = Field(default="好的", description="Response message")
    slots: Optional[list[MusicMessage]] = Field(default=None, description="List of music messages")

class HistoryMessage(BaseModel):
    query: Optional[str] = Field(default=None, description="")
    answer:Optional[str] = Field(default=None, description="")
    answer_tokens:int = Field(default=0, description="")
    error: Optional[str] = Field(default=None, description="")
    type: Optional[int] = Field(default=0, description="")