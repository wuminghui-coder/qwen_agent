import uuid
from typing import Any, List
import random
from sqlmodel import Session, select
import string
from core.security import get_password_hash, verify_password
from models.model import  User, Message, Conversation
from datetime import datetime, timezone
from sqlalchemy.orm import selectinload
import json
from fields.message_type import MessageType, BertType
import logging
logger = logging.getLogger(__name__)
def create_user(*, session: Session, user_name: str) -> User:
    create_user = User(
        updated_at = datetime.now(timezone.utc).replace(tzinfo=None),
        name = user_name,
    )
    session.add(create_user)
    session.commit()
    session.refresh(create_user)

    return create_user

def update_user(*, session: Session, user_id: str, name:str) -> User:
    db_user = session.get(User, user_id)
    if not db_user:
        return None 

    db_user.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db_user.name = name
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

def delete_user(*, session: Session, user_id: str) -> bool:
    db_user = session.get(User, user_id)
    if not db_user:
        return False

    session.delete(db_user)
    session.commit()

    return True

def get_id_of_user(*, session: Session, user_id: str) -> User:
    db_user = session.get(User, user_id)
    if not db_user:
        return False
    
    return db_user

def get_name_of_user(*, session: Session, keyword: str) ->list[User]:
    stmt = select(User).order_by(User.created_at.desc()).where(User.name.like(f"%{keyword}%"))  # 模糊查询
    return session.exec(stmt).all()


def get_uset_by_name(session: Session, name: str) -> User:
    stmt = select(User).order_by(User.created_at.desc()).where(User.name == name).options(selectinload(User.conversation))   # 模糊查询
    return session.exec(stmt).first()


def get_all_user(session: Session) ->list[User]:
    stmt = select(User).order_by(User.created_at.desc())
    return session.exec(stmt).all()

def create_conversation(*, session: Session, user_id: str, name: str) -> Conversation:
    db_user = get_id_of_user(session=session, user_id=user_id)
    if not db_user:
        return None
    
    conversation = Conversation(
        name=name,
        owner=db_user,
        owner_id=user_id
    )

    #memory = Memory(
    #    conversation_id = conversation.id
    #)

    session.add(conversation)

    session.commit()
    session.refresh(conversation)

    return conversation

def update_conversation(*, session: Session, conversation_id: str, name: str) -> Conversation:
    db_conversation = session.get(Conversation, conversation_id)
    if not db_conversation:
        return None 

    db_conversation.name = name
    db_conversation.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(db_conversation)
    session.commit()
    session.refresh(db_conversation)

    return db_conversation

def delete_conversation(*, session: Session, conversation_id: str) -> bool:
    db_conversation = session.get(Conversation, conversation_id)
    if not db_conversation:
        return False

    session.delete(db_conversation)
    session.commit()

    return True

def get_conversation(*, session: Session, conversation_id: str) -> Conversation:
    db_conversation = session.get(Conversation, conversation_id)
    if not db_conversation:
        return False
    
    return db_conversation

def get_user_conversation(*, session: Session, user_id: str) -> list[Conversation]:
    stmt = select(Conversation).where(Conversation.owner_id == user_id).order_by(Conversation.created_at.desc())
    return session.exec(stmt).all()

def get_time_of_conversationn(*, session: Session, user_id: str) ->list[Conversation]:
    stmt = select(Conversation).where(Conversation.owner_id == user_id).order_by(Conversation.created_at.desc())
    return session.exec(stmt).all()

def create_message(*, session: Session, conversation_id: str, args:dict)->Message:
    db_conversation = session.get(Conversation, conversation_id)
    if not db_conversation:
        return None 
    
    db_message = Message(
        owner=db_conversation,
        owner_id=conversation_id,
        query=args.get('query'),
        answer=args.get('answer'),
        answer_tokens=args.get('answer_tokens'),
        error=args.get('error')
    )

    session.add(db_message)
    session.commit()
    session.refresh(db_message)

    return db_message


def update_message(*, session: Session, message_id: str, args: dict)->Message:
    db_message = session.get(Message, message_id)
    if not db_message:
        return None 
    
    if args.get('query'):
        db_message.query = args.get('query')
    if args.get('answer'):
        db_message.answer = args.get('answer')
    if args.get('answer_tokens'):
        db_message.answer_tokens = args.get('answer_tokens')
    if args.get('error'):
        db_message.error = args.get('error')

    db_message.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

    session.add(db_message)
    session.commit()
    session.refresh(db_message)

    return db_message

def delete_message(*, session: Session, message_id: str) -> bool:
    db_messag = session.get(Message, message_id)
    if not db_messag:
        return False

    session.delete(db_messag)
    session.commit()

    return True

def get_message_of_id(*, session: Session, message_id: str)->Message:
    db_message = session.get(Message, message_id)
    if not db_message:
        return False
    
    return db_message

##按时间获取全部消息
def get_time_of_message(*, session: Session, conversation_id: str)->list[Message]:
    stmt = select(Message).where(Message.owner_id == conversation_id).order_by(Message.created_at.desc())
    return session.exec(stmt).all()

##分页查询会问下的消息
def get_paginate_message(*, session: Session, conversation_id: str, page: int, page_size:int)->list[Message]:
    stmt = select(Message).where(Message.owner_id == conversation_id).order_by(Message.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    messages = session.exec(stmt).all()
    return messages

##获取前limit条会问下的消息
def get_desc_message(*, session: Session, conversation_id: str, limit:int)->list[Message]:
    stmt = select(Message).where(Message.owner_id == conversation_id).order_by(Message.created_at).limit(limit)
    return session.exec(stmt).all()

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
