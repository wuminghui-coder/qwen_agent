
from models.model import  User, Message, Conversation, Memory
from sqlmodel import Session, select
from typing import Any, List, Optional
from datetime import datetime, timezone
import logging
import uuid
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)

class UserServiceUpdate:
    @staticmethod
    def create_user(session: Session, user_name: str)->Optional[User]:
        new_user = User(
            name = user_name,
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    
    @staticmethod
    def delete_user(session: Session, user_id: str)->bool:
        db_user = session.get(User, user_id)
        if not db_user:
            return False
        
        session.delete(db_user)
        session.commit()

        return True
    
    @staticmethod
    def get_user_by_id(session: Session, user_id: str)->Optional[User]:
        return session.get(User, user_id)
    
    @staticmethod
    def get_user_by_name(session: Session, name: str)->Optional[User]:
        stmt = select(User).order_by(User.created_at.desc()).where(User.name == name).options(selectinload(User.conversation))
        return session.exec(stmt).first()
    
    @staticmethod
    def get_user_by_like_name(session: Session, name: str)->Optional[User]:
        stmt = select(User).order_by(User.created_at.desc()).where(User.name.like(f"%{name}%"))  # 模糊查询
        return session.exec(stmt).first()
    
    @staticmethod
    def get_all_user(session: Session)->Optional[list[User]]:
        stmt = select(User).order_by(User.created_at.desc())
        return session.exec(stmt).all()