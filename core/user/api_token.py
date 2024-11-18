from models.model import  User, Message, Conversation, Memory, ApiToken, App
from sqlmodel import Session, select
from typing import Any, List, Optional
from datetime import datetime, timezone
import logging
import uuid
from sqlalchemy.orm import selectinload
from core.user.user import UserServiceUpdate
from core.user.memory import MemoryServiceUpdate
from core.user.conversation import MemoryServiceUpdate
from core.util import generate_random_id
from fastapi import Depends, HTTPException, status, Request

class ApiTokenServiceUpdate:
    @staticmethod
    def create_api_token(session: Session, app_id: str)->Optional[ApiToken]:
        db_app = session.get(App, app_id)
        if not db_app :
            return None
        
        api_token = ApiToken(
            app_id=db_app.id,
            owner=db_app,
            token="app-" + generate_random_id(24)
        )

        session.add(api_token)
        session.commit()
        session.refresh(api_token)
    
        return api_token


    @staticmethod
    def verify_token(session: Session, token:str)->Optional[str]:
        api_token = session.exec(select(ApiToken).where(ApiToken.token == token)).first()
        return str(api_token.app_id)
    @staticmethod
    def get_all_app_token(session: Session, app_id: str)->Optional[list[ApiToken]]:
        db_app = session.get(App, app_id)
        if not db_app :
            return None
        
        return session.exec(select(ApiToken).where(ApiToken.app_id == db_app.id)).all()
