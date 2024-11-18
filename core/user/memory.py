from models.model import  User, Message, Conversation, Memory
from sqlmodel import Session, select
from typing import Any, List, Optional
from datetime import datetime, timezone
import logging
import uuid
from sqlalchemy.orm import selectinload
from core.user.user import UserServiceUpdate
from fields.app_fields import MusicMessage,ResponesMessage,HistoryMessage
import json

logger = logging.getLogger(__name__)

class MemoryServiceUpdate:
    @staticmethod
    def create_memory(session: Session, conversation_id: str)->Optional[Memory]:
        db_conversation = session.get(Conversation, conversation_id)
        if not db_conversation:
            return None 
        
        from app import app_config
        play_list = app_config["wymusci"].get_new_of_songs(20)
        if not play_list:
            return None

        memory = Memory(
            owner_id=conversation_id,
            play_list=json.dumps(play_list, ensure_ascii=False),
            play_len=len(play_list),
            index=0
        )

        session.add(memory)
        session.commit()
        session.refresh(memory)

        return memory
    
    @staticmethod
    def save_repones_to_memory(session: Session, 
                               conversation_id:str, 
                               message: ResponesMessage)->Optional[Memory]:
        memory = MemoryServiceUpdate.get_memory_by_conversation_id(session=session, 
                                                                   conversation_id=conversation_id)
        if not memory or not message.slots:
            return None
        
        memory.add_list_to_playlist(message.slots)

        session.add(memory)
        session.commit()
        session.refresh(memory)

        return memory
    
    @staticmethod
    def save_music_to_memory(session: Session, 
                               conversation_id:str, 
                               message: list[MusicMessage])->Optional[Memory]:
        memory = MemoryServiceUpdate.get_memory_by_conversation_id(session=session, 
                                                                   conversation_id=conversation_id)
        if not memory or not message:
            return None
        
        memory.add_list_to_playlist(message)

        session.add(memory)
        session.commit()
        session.refresh(memory)

        return memory

    @staticmethod
    def get_memory_by_conversation_id(session: Session, conversation_id: str)->Optional[Memory]:
        stmt = select(Memory).where(Memory.owner_id == conversation_id)
        return session.exec(stmt).first()
    
    @staticmethod
    def get_memory_current_song(session: Session, conversation_id: str)->Optional[MusicMessage]:
        memory = MemoryServiceUpdate.get_memory_by_conversation_id(session=session, 
                                                                   conversation_id=conversation_id)
        if not memory:
            return None
            
        return memory.get_current_song

    @staticmethod
    def get_memory_next_song(session: Session, conversation_id: str)->Optional[MusicMessage]:
        memory = MemoryServiceUpdate.get_memory_by_conversation_id(session=session, 
                                                                   conversation_id=conversation_id)
        if not memory:
            return None
            
        return memory.get_next_song

    @staticmethod
    def get_memory_pre_song(session: Session, conversation_id: str)->Optional[MusicMessage]:
        memory = MemoryServiceUpdate.get_memory_by_conversation_id(session=session, 
                                                                   conversation_id=conversation_id)
        if not memory:
            return None
            
        return memory.get_pre_song
    
    @staticmethod
    def get_memory_playlist(session: Session, conversation_id: str)->Optional[str]:
        memory = MemoryServiceUpdate.get_memory_by_conversation_id(session=session, 
                                                                   conversation_id=conversation_id)
        if not memory:
            return None
        
        play_list = memory.get_play_list

        chinese_numerals = [
            '零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
            '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
            '二十一', '二十二', '二十三', '二十四', '二十五', '二十六', '二十七', '二十八', '二十九', '三十'
        ]

        play_list = play_list[memory.index:memory.index + 20]

        play_list_string = '，'.join(f'第{chinese_numerals[index + 1]}首：{item["song_name"]}' for index, item in enumerate(play_list))

        return "播放列表:" + play_list_string
    
        

