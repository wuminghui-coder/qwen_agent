from models.model import  User, Message, Conversation, Memory
from sqlmodel import Session, select
from typing import Any, List, Optional
from datetime import datetime, timezone
import logging
import uuid
from sqlalchemy.orm import selectinload
from core.user.user import UserServiceUpdate
logger = logging.getLogger(__name__)

class MessageServiceUpdate:
    @staticmethod
    def create_message(session: Session, conversation_id: str, args:dict)->Optional[Message]:
        if not args:
            return None
        
        db_conversation = session.get(Conversation, conversation_id)
        if not db_conversation:
            return None 
        
        db_message = Message(
            owner=db_conversation,
            owner_id=conversation_id,
            query=args.get('query'),
            answer=args.get('answer'),
            answer_tokens=args.get('answer_tokens'),
            error=args.get('error'),
            type=args.get('type'),
        )

        session.add(db_message)
        session.commit()
        session.refresh(db_message)

        return db_message

    @staticmethod
    def update_message(session: Session, message_id: str, args: dict)->Optional[Message]:
        if not args:
            return None
        
        db_message = session.get(Message, message_id)
        if not db_message:
            return None 
        
        db_message.query = args.get('query')
        db_message.answer = args.get('answer')
        db_message.answer_tokens = args.get('answer_tokens')
        db_message.error = args.get('error')
        db_message.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

        session.add(db_message)
        session.commit()
        session.refresh(db_message)

        return db_message
    
    @staticmethod
    def delete_message(session: Session, message_id: str)->bool:
        db_messag = session.get(Message, message_id)
        if not db_messag:
            return False

        session.delete(db_messag)
        session.commit()

        return True
    
    @staticmethod
    def get_message_by_id(session: Session, message_id: str)->Optional[Message]:
        db_message = session.get(Message, message_id)
        if not db_message:
            return False
        
        return db_message

    ##按时间获取全部消息
    @staticmethod
    def get_message_by_conversation_id(session: Session, conversation_id: str)->Optional[list[Message]]:
        stmt = select(Message).where(Message.owner_id == conversation_id).order_by(Message.created_at.desc())
        return session.exec(stmt).all()

    ##分页查询会问下的消息
    @staticmethod
    def get_paginate_message(session: Session, conversation_id: str, page: int, page_size:int)->list[Message]:
        stmt = select(Message).where(Message.owner_id == conversation_id).order_by(Message.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        messages = session.exec(stmt).all()
        return messages

    ##获取前limit条会问下的消息
    @staticmethod
    def get_desc_message(session: Session, conversation_id: str, limit:int)->list[Message]:
        stmt = select(Message).where(Message.owner_id == conversation_id).order_by(Message.created_at).limit(limit)
        return session.exec(stmt).all()

