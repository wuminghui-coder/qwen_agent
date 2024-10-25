import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy import JSON
from sqlalchemy import Index, PrimaryKeyConstraint
from sqlalchemy import Column, TEXT, BigInteger
import json

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
   