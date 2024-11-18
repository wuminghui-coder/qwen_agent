import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy import JSON
from sqlalchemy import Index, PrimaryKeyConstraint
from sqlalchemy import Column, TEXT, BigInteger, SmallInteger
import json
import logging
from fields.app_fields import MusicMessage,ResponesMessage,HistoryMessage, HistoryType

logger = logging.getLogger(__name__)

class User(SQLModel, table=True):
    __tablename__ = 'user'  # 指定表名
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_pkey'),
        Index('user_idx', 'name', 'created_at')
    )
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=255, sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})  # 更新时间
    conversation: list["Conversation"] = Relationship(
        back_populates="owner", 
        sa_relationship_kwargs={"passive_deletes": True, "lazy": "select", "cascade": "all, delete-orphan"}
    )

class Conversation(SQLModel, table=True):
    __tablename__ = 'conversation'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='conversation_pkey'),
        Index('conversation_idx', 'user_id', 'created_at', "owner_id")
    )

    name: str = Field(default=None, sa_column=Column(TEXT))
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4)

    owner_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="conversation")

    messages: list["Message"] = Relationship(
        back_populates="owner", 
        sa_relationship_kwargs={"passive_deletes": True, "lazy": "select", "cascade": "all, delete-orphan"}
    )
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})  # 更新时间


class Message(SQLModel, table=True):
    __tablename__ = 'messages'  # 指定表名
    __table_args__ = (
        PrimaryKeyConstraint('id', name='message_pkey'),  # 主键约束
        Index('message_uset_idx', 'user_id', 'created_at'),               # 索引
        Index('message_conversation_idx', 'owner_id'),  # 索引
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: Optional[uuid.UUID] = Field(default=None, foreign_key="conversation.id")
    owner: Optional[Conversation] = Relationship(back_populates="messages")
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})  # 更新时间

    query : str  = Field(default=None, sa_column=Column(TEXT))
    answer : str = Field(default=None, sa_column=Column(TEXT))
    answer_tokens : int = Field(default=None, sa_column=Column(BigInteger))
    error : str  = Field(default=None, sa_column=Column(TEXT))
    type : int   = Field(default=0, sa_column=Column(SmallInteger))


class Memory(SQLModel, table=True):
    __tablename__ = 'memory'  # 指定表名

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: Optional[uuid.UUID] = Field(default=None, foreign_key="conversation.id")
   
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})  # 更新时间

    play_len  : int  = Field(default=0, sa_column=Column(BigInteger))
    play_list : str  = Field(default=json.dumps([]), sa_column=Column(TEXT))
    index     : int  = Field(default=0,   sa_column=Column(BigInteger))
    special   : str  = Field(default=json.dumps([]), sa_column=Column(TEXT))
    @property
    def get_play_list(self)->Optional[list]:
        return json.loads(self.play_list)
    
    def add_list_to_playlist(self, add_play: list[MusicMessage]):
        play_list = self.get_play_list

        self.play_len += len(add_play)

        for add_item in reversed(add_play):
            play_list.insert(self.index, add_item.dict())

        self.play_list = json.dumps(play_list, ensure_ascii=False)
    @property
    def get_next_song(self)->Optional[MusicMessage]:
        play_list = self.get_play_list
        if not play_list:
            return None
      
        if self.index + 1 < len(play_list):
            self.index += 1
        else:
            self.index = 0
        return MusicMessage.parse_obj(play_list[self.index])
    @property
    def get_pre_song(self)->Optional[MusicMessage]:
        play_list = self.get_play_list
        if not play_list:
            return None
        
        if self.index - 1 >= 0:
            self.index -= 1
        else:
            self.index = len(play_list) - 1
        return MusicMessage.parse_obj(play_list[self.index])
    @property
    def get_current_song(self)->Optional[MusicMessage]:
        play_list = self.get_play_list
        if not play_list:
            return None

        return MusicMessage.parse_obj(play_list[self.index])
    
class App(SQLModel, table=True):
    __tablename__ = 'app'  # 指定表名
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})  # 更新时间
    
    name : str  = Field(default=None, sa_column=Column(TEXT))
    describe: str  = Field(default=None, sa_column=Column(TEXT))
    version: str  = Field(default=None, sa_column=Column(TEXT))
    icon: str  = Field(default=None, sa_column=Column(TEXT))
    url: str  = Field(default=None, sa_column=Column(TEXT))
    api_tokens: List["ApiToken"] = Relationship(
        back_populates="owner", 
        sa_relationship_kwargs={"passive_deletes": True, "lazy": "select", "cascade": "all, delete-orphan"}
    )

class ApiToken(SQLModel, table=True):
    __tablename__ = 'api_tokens'
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    app_id: Optional[uuid.UUID] = Field(default=None, foreign_key="app.id")
    owner: Optional[App] = Relationship(back_populates="api_tokens")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})  # 更新时间

    token: str  = Field(default=None, sa_column=Column(TEXT))


class MusicData(SQLModel, table=True):
    __tablename__ = 'music_data'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='music_pkey'),  # 主键约束
        Index('music_user_idx', 'song_id', 'created_at', 'artist', 'song_name'),    # 索引
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    song_id: int   = Field(default=None, sa_column=Column(BigInteger))
    song_name: str  = Field(default=None, sa_column=Column(TEXT))
    artist: str  = Field(default=None, sa_column=Column(TEXT))
    lyric:str  = Field(default=None, sa_column=Column(TEXT))
    image:str  = Field(default=None, sa_column=Column(TEXT))
    format:str  = Field(default="mp3", sa_column=Column(TEXT))

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})  # 更新时间


class AudioData(SQLModel, table=True):
    __tablename__ = 'audio_data'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='audio_pkey'),  # 主键约束
        Index('audio_user_idx', 'music_id'),    # 索引
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    music_id: Optional[uuid.UUID] = Field(default=None)

    data:bytes = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})  # 更新时间