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


class AppServiceUpdate:
    @staticmethod
    def create_app(session: Session, app_name: str,  describe: str, version: str, icon: str, url: str)->Optional[App]:
        app = App(
            name=app_name,
            describe=describe,
            version=version,
            url=url,
            icon=icon
        )

        session.add(app)
        session.commit()
        session.refresh(app)
    
        return app
    
    @staticmethod
    def get_all_user(session: Session)->Optional[list[App]]:
        return session.exec(select(App).order_by(App.created_at.desc())).all()
    
    @staticmethod
    def get_app_by_id(session: Session, app_id: str)->Optional[App]:
        return session.get(App, app_id)