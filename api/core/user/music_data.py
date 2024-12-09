from models.model import  MusicData, AudioData
from sqlmodel import Session, select
from typing import Any, List, Optional
from datetime import datetime, timezone
import logging
from fields.app_fields import MusicMessage
import requests

logger = logging.getLogger(__name__)

class MusicServiceUpdate:
    @staticmethod
    def create_db_music(music_info: MusicMessage, session: Session)->Optional[MusicData]:
        db_music = MusicServiceUpdate.get_music_by_song_id(session, music_info.song_id)
        if db_music:
            return db_music
        
        if not music_info.song_url:
            return None
        
        response = requests.get(music_info.song_url)
        if response.status_code != 200:
            return None

        db_music = MusicData(
            song_id   = music_info.song_id,
            song_name = music_info.song_name,
            artist    = music_info.artist,
            lyric     = music_info.lyric,
            image     = music_info.image,
            format    = ".flac" if ".flac" in music_info.song_url else ".mp3"
        )

        db_audio = AudioData(music_id=db_music.id, 
                            data=response.content)
        
        session.add(db_audio)
        session.add(db_music)

        session.commit()
        session.refresh(db_music)
        session.refresh(db_audio)

        return db_music
    
    @staticmethod
    def get_music_by_song_id(session: Session, song_id: str)->Optional[MusicData]:
        return session.exec(select(MusicData).where(MusicData.song_id == song_id)).first()
    
    @staticmethod
    def get_music_by_id(session: Session, music_id: str)->Optional[MusicData]:
        return session.exec(select(MusicData).where(MusicData.id == music_id)).first()
    
    @staticmethod
    def get_music_by_name(session: Session, song_name: str)->Optional[list[MusicData]]:
        return session.exec(select(MusicData).where(MusicData.song_name == song_name).distinct(MusicData.song_id)).all()

    @staticmethod
    def get_audio_by_music_id(session: Session, music_id: str)->Optional[AudioData]:
        return session.exec(select(AudioData).where(AudioData.music_id == music_id)).first()