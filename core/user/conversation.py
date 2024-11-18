from models.model import  User, Message, Conversation, Memory
from sqlmodel import Session, select
from typing import Any, List, Optional
from datetime import datetime, timezone
import logging
import uuid
from sqlalchemy.orm import selectinload
from core.user.user import UserServiceUpdate
from core.user.memory import MemoryServiceUpdate
from core.user.conversation import MemoryServiceUpdate

logger = logging.getLogger(__name__)

class ConversationServiceUpdate:
    @staticmethod
    def create_conversation(session: Session, user_id: str, name: str)->Optional[Conversation]:
        db_user = UserServiceUpdate.get_user_by_id(session=session, user_id=user_id)
        if not db_user:
            return None
        
        conversation = Conversation(
            name=name,
            owner=db_user,
            owner_id=user_id
        )

        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        MemoryServiceUpdate.create_memory(session=session, 
                                          conversation_id=conversation.id)
        
        return conversation
    @staticmethod
    def update_conversation(session: Session, conversation_id: str, name: str)->Optional[Conversation]:
        db_conversation = session.get(Conversation, conversation_id)
        if not db_conversation:
            return None 

        db_conversation.name = name
        db_conversation.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        session.add(db_conversation)
        session.commit()
        session.refresh(db_conversation)

        return db_conversation
    @staticmethod
    def delete_conversation(session: Session, conversation_id: str)-> bool:
        db_conversation = session.get(Conversation, conversation_id)
        if not db_conversation:
            return False

        session.delete(db_conversation)
        session.commit()

        return True
    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: str) -> Optional[Conversation]:
        db_conversation = session.get(Conversation, conversation_id)
        if not db_conversation:
            return False
        
        return db_conversation
    
    @staticmethod
    def get_conversation_by_user_id(session: Session, user_id: str) -> list[Conversation]:
        stmt = select(Conversation).where(Conversation.owner_id == user_id).order_by(Conversation.created_at.desc())
        return session.exec(stmt).all()
    