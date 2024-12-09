from typing import Optional
import logging
from fields.message_type import MessageType, BertType
from core.api_service.music_api import MusicLevel
from fields.app_fields import MusicMessage,ResponesMessage,HistoryMessage
from extensions.exten_sql import SessionDep
from core.user.memory import MemoryServiceUpdate
from core.user.message import MessageServiceUpdate
from core.api_service.categorize import bert_categorize
from core.user.conversation import ConversationServiceUpdate
from core.user.user import UserServiceUpdate
from core.user.music_data import MusicServiceUpdate
from sqlmodel import Session, select
from core.util import is_valid_uuid, upload_lyric_file
from tasks.db_music_task import creat_db_music_task
from core.tools_call.tools_service import tools_service
from extensions.exten_mem0 import mem0_api
from config.app_config import settings
import re
import random
from core.prompt import (
    MUSIC_PROMPT, 
    CHAT_PROMPT,
    MUSIC_PROMPT_TEST,
    ARTIST_PROMPT_TEST, 
    WEATHER_PROMPT,
    SONG_PROMPT
)

logger = logging.getLogger(__name__)

class MusicAgent():
    def __init__(self, session: SessionDep, conversation_id:str, user: str):
        self.session = session
        self.conversation_id = conversation_id
        self.user = user

    def get_song_message(self, mtype:MessageType, music_list:list[MusicMessage])->Optional[ResponesMessage]:
        song_info = MusicServiceUpdate.get_music_by_song_id(session=self.session, 
                                                            song_id = music_list[0].song_id)
        if song_info:
            music_list[0].song_url = "http://172.30.13.160:5001/music/song_id/" + str(song_info.id) + song_info.format
            music_list[0].lyric    = song_info.lyric
            music_list[0].image    = song_info.image
        else:
            from app import app_config
            song_url = app_config["wymusci"].get_song_of_url(music_list[0].song_id, MusicLevel.LOSSLESS)
            if not song_url:
                logger.error(f"Get song of url failed: {music_list[0].song_id}")
                return None

            song_lyric = app_config["wymusci"].get_song_of_lyrics(music_list[0].song_id)
            if not song_lyric:
                logger.error(f"Get song of lyrics failed: {music_list[0].song_id}")

            song_detail = app_config["wymusci"].get_song_detail_of_id(music_list[0].song_id)
            if not song_detail:
                logger.error(f"Get song of detail failed: {music_list[0].song_id}")

            music_list[0].song_url = song_url
            music_list[0].lyric    = song_lyric
            music_list[0].image    = song_detail["image"]

            creat_db_music_task.delay(music_list[0].dict())

        return ResponesMessage(message="好的，正在播放" + music_list[0].artist + "的《" + music_list[0].song_name + "》",
                              type=mtype.value, 
                              slots=music_list, 
                              user = self.user, 
                              conversation_id=self.conversation_id)
        
    def get_song_by_name_and_artist(self, song_name:str, artist:str)->Optional[ResponesMessage]:
        song_name = song_name.replace("《", "").replace("》", "")

        from app import app_config
        song_info = app_config["wymusci"].get_search_match_of_song(song_name, artist)
        if not song_info:
            logger.error("get_search_match_of_song error")
            return None
        
        music = MusicMessage.parse_obj(song_info)

        return self.get_song_message(mtype=MessageType.PLAY_MUSIC, 
                                     music_list=[music])

    def get_search_song_result(self, song_name:str)->Optional[ResponesMessage]:
        song_name = song_name.replace("《", "").replace("》", "")

        from app import app_config
        play_list = app_config["wymusci"].get_search_multimatch(song_name)
        if not play_list:
            logger.error("get song list error")
            return None
            
        music_messages = [MusicMessage.parse_obj(music_info) for music_info in play_list]
        
        return self.get_song_message(mtype=MessageType.PLAY_MUSIC, 
                                 music_list=music_messages)
    
    def get_search_playlist_by_name(self, keywords:str)->Optional[ResponesMessage]:
        keywords = keywords.replace("《", "").replace("》", "")

        from app import app_config
        play_list = app_config["wymusci"].get_highquality_of_playlist(keywords=keywords, limit=10)
        if not play_list:
            logger.error("get song highquality list error")
            return None
        
        music_list = app_config["wymusci"].get_playlist_of_songs(play_list[0]["id"], 10)
        if not music_list:
            logger.error("get song list error")
            return None
        
        music_messages = [MusicMessage.parse_obj(music_info) for music_info in music_list]
        
        return self.get_song_message(mtype=MessageType.PLAY_MUSIC, 
                                     music_list=music_messages)
    
    def get_song_by_artist(self, artist:str)->Optional[ResponesMessage]:
        from app import app_config
        artist_resp = app_config["wymusci"].get_search_of_artist(artist)
        if not artist_resp:
            logger.error("get_search_of_artist error")
            return None
            
        play_list = app_config["wymusci"].get_artist_of_playlist(artist_resp["id"], 20)
        if not play_list:
            logger.error("get_artist_of_playlist error")
            return None

        music_messages = [MusicMessage.parse_obj(music_info) for music_info in play_list]
        
        return self.get_song_message(mtype=MessageType.PLAY_MUSIC, 
                                 music_list=music_messages)
    
    def get_recommend_songs(self):
        from app import app_config
        play_list = app_config["wymusci"].get_new_of_songs(20)
        if not play_list:
            logger.error("get_new_of_songs error")
            return None
        
        random.shuffle(play_list)

        music_messages = [MusicMessage.parse_obj(music_info) for music_info in play_list]
      
        return self.get_song_message(mtype=MessageType.PLAY_MUSIC, 
                                    music_list=music_messages)

    def get_song_by_name(self, song_name:str)->Optional[ResponesMessage]:
        from app import app_config
        play_list = app_config["wymusci"].get_search_song_by_name(song_name)
        if not play_list:
            logger.error("get_search_song_by_name error")
            return None

        music_messages = [MusicMessage.parse_obj(music_info) for music_info in play_list]
        #music_messages = [MusicMessage.parse_obj(play_list[0])]

        return self.get_song_message(mtype=MessageType.PLAY_MUSIC, 
                                 music_list=music_messages)

    def get_lyric_of_song(self, message: dict)->Optional[ResponesMessage]:
        if not message.get("song_name"):
            music_message = MemoryServiceUpdate.get_memory_current_song(session=self.session, 
                                                                conversation_id=self.conversation_id)
            if not music_message:
                logger.error("get_memory_current_song error")
                return None
            
            message["song_name"] = music_message.song_name

        message["song_name"] = message["song_name"].replace("《", "").replace("》", "")

        from app import app_config
        resp = app_config["wymusci"].get_search_match_of_song(message["song_name"], None)
        if not resp:
            logger.error("get_search_match_of_song error")
            return None

        song_lyric = app_config["wymusci"].get_song_of_lyrics(resp["song_id"])
        if not song_lyric:
            logger.error("get_song_of_lyrics error")
            return None
        
        song_lyric = re.sub(r'\[.*?\]', '', song_lyric)
        song_lyric = song_lyric.replace('\n', '，').strip()

        self.save_chat_history(
            history=HistoryMessage(answer="用户正在查询" + resp["artist"]  + "的" + resp["song_name"] + "的歌词")
        )

        music = MusicMessage(song_id=resp["song_id"], 
                            artist=resp["artist"], 
                            song_name=resp["song_name"], 
                            lyric=song_lyric)

        return ResponesMessage(message="好的，" + resp["song_name"] + "的歌词是：" + song_lyric,
                               type=MessageType.LYRIC.value, 
                               slots=[music], 
                               user = self.user, 
                               conversation_id=self.conversation_id)


    def save_chat_history(self, history: HistoryMessage):
        new_message = MessageServiceUpdate.create_message(session=self.session, 
                                                        conversation_id=self.conversation_id, 
                                                        args=history.dict())
        if not new_message:
            logger.error(f"Save chat history failed: {self.conversation_id}")

    def get_db_song_repones(self, song_name:Optional[str])->Optional[ResponesMessage]:
        if not song_name:
            return None
        
        play_list = MusicServiceUpdate.get_music_by_name(self.session, song_name)
        if not play_list:
            return None
        
        music_messages = [MusicMessage(song_id = song_info.song_id,
                                       song_name = song_info.song_name,
                                       artist = song_info.artist,
                                       lyric = song_info.lyric,
                                       image = song_info.image,
                                       song_url = "http://172.30.13.160:5001/music/song_id/" + str(song_info.id) + song_info.format
                        ) for song_info in play_list]

        return ResponesMessage(message="好的，正在播放" + play_list[0].artist + "的《" + play_list[0].song_name + "》",
                              type=MessageType.PLAY_MUSIC, 
                              slots=music_messages, 
                              user = self.user, 
                              conversation_id=self.conversation_id)

    def get_play_music(self, message: dict)->Optional[ResponesMessage]:
        if message.get("artist") and not message.get("song_name"):
            respones = self.get_song_by_artist(message.get("artist"))
            if not respones:
                return None
            MemoryServiceUpdate.save_repones_to_memory(session=self.session,
                                                        conversation_id=self.conversation_id,
                                                        message=respones)
        elif message.get("artist") and message.get("song_name"):
            respones = self.get_song_by_name_and_artist(song_name=message.get("song_name"), 
                                            artist=message.get("artist"))
            if not respones:
                return None
            
            MemoryServiceUpdate.save_repones_to_memory(session=self.session,
                                                    conversation_id=self.conversation_id,
                                                    message=respones)
        elif not message.get("artist") and message.get("song_name"):
            respones = self.get_db_song_repones(message.get("song_name"))
            if not respones:
                respones = self.get_song_by_name(message.get("song_name"))

            MemoryServiceUpdate.save_repones_to_memory(session=self.session,
                                                        conversation_id=self.conversation_id,
                                                        message=respones)
            return respones
        else:
            respones = self.get_db_song_repones(message.get("song_name"))
            if not respones:
                play_history = MemoryServiceUpdate.get_memory_playlist(session=self.session, 
                                                                    conversation_id=self.conversation_id)
                respones = self.qwen_tools_call_chat(query=message.get("query"), 
                                                    history=play_history,
                                                    prompt=SONG_PROMPT)
                if not respones:
                    return None
            
            MemoryServiceUpdate.save_repones_to_memory(session=self.session,
                                                      conversation_id=self.conversation_id,
                                                      message=respones)
                
        self.save_chat_history(
            history=HistoryMessage(answer="用户正在听" + respones.slots[0].artist + "的" + respones.slots[0].song_name)
        )
        return respones


    def get_artist_of_playlist_result(self, message: dict)->Optional[ResponesMessage]:
        if not message.get("artist"):
            music_message = MemoryServiceUpdate.get_memory_current_song(session=self.session, 
                                                                conversation_id=self.conversation_id)
            if not music_message:
                return None

            message["artist"] = music_message.artist

        from app import app_config
        artist_resp = app_config["wymusci"].get_search_of_artist(message.get("artist"))
        if not artist_resp:
            return None
            
        play_list = app_config["wymusci"].get_artist_of_playlist(artist_resp["id"], 15)
        if not play_list:
            return None
        
        songlist = "，".join(x["song_name"] for x in play_list)

        self.save_chat_history(
            history=HistoryMessage(answer="用户正在查询" + artist_resp["artist"] + "的歌单")
        )

        music_messages = [MusicMessage.parse_obj(music_info) for music_info in play_list]

        MemoryServiceUpdate.save_music_to_memory(session=self.session,
                                                conversation_id=self.conversation_id, 
                                                message=music_messages)
        
        return ResponesMessage(message="好的，" + artist_resp["artist"] + "的歌曲有" + songlist,
                              type=MessageType.PLAYLIST.value, 
                              slots=music_messages, 
                              user = self.user, 
                              conversation_id=self.conversation_id)
    def get_llm_music(self, message: dict)->Optional[ResponesMessage]:
        respones = self.get_db_song_repones(message.get("song_name"))
        if not respones:
            respones = self.qwen_tools_call_chat(query=message.get("query"), 
                                                history=None,
                                                prompt=SONG_PROMPT)
            if not respones:
                return None

        self.save_chat_history(
            history=HistoryMessage(answer="用户正在听" + respones.slots[0].artist + "的" + respones.slots[0].song_name)
        )

        MemoryServiceUpdate.save_repones_to_memory(session=self.session,
                                                    conversation_id=self.conversation_id,
                                                    message=respones)
        return respones

    def get_story_result(self, message: dict)->Optional[ResponesMessage]:
        if not message.get("song_name"):
            return None

        from app import app_config
        #story_list = app_config["ximalaya"].get_search_tracks(message.get("song_name"))get_albums_story
        story_list = app_config["ximalaya"].get_albums_story(message.get("song_name"))
        if not story_list:
            logger.error("get story_result error")
            return None
            
        respones = ResponesMessage(message="好的，正在播放《" + story_list[0]["song_name"] + "》",
                                    type=MessageType.PLAY_STORY.value, 
                                    slots=[MusicMessage.parse_obj(music_info) for music_info in story_list], 
                                    user = self.user, 
                                    conversation_id=self.conversation_id)
        
        MemoryServiceUpdate.save_repones_to_memory(session=self.session,
                                                    conversation_id=self.conversation_id,
                                                    message=respones) 
        return respones

    def get_artist_of_detail_result(self, message: dict)->Optional[ResponesMessage]:
        if not message.get("artist"):
            music_message = MemoryServiceUpdate.get_memory_current_song(session=self.session, 
                                                                        conversation_id=self.conversation_id)
            if not music_message:
                return None

            message["artist"] = music_message.artist

        from app import app_config
        artist_resp = app_config["wymusci"].get_search_of_artist(message.get("artist"))
        if not artist_resp:
            logger.error("get_search_of_artist error")
            return None
            
        artist_detail = app_config["wymusci"].get_other_artist_of_detail(artist_resp["id"])
        if not artist_detail:
            logger.error("get_other_artist_of_detail error")
            return None
        
        self.save_chat_history(
            history=HistoryMessage(answer="用户正在查询歌手" + message.get("artist") + "的个人介绍")
        )

        return ResponesMessage(message="好的，" + artist_detail,
                              type=MessageType.ARTIST_INFO.value,  
                              user = self.user, 
                              conversation_id=self.conversation_id)

    def get_weather_result(self, message: dict)->Optional[ResponesMessage]:
        if not message.get("weather"):
            return None
        
        from app import app_config
        resp = app_config["weather"].get_now_weather(message.get("weather"))
        if not resp:
            logger.error("get_now_weather error")
            return None
        
        self.save_chat_history(
            history=HistoryMessage(answer=resp, query=message.get("query"))
        )

        return ResponesMessage(message=resp,
                              user = self.user,
                              type=MessageType.WEATHER.value,  
                              conversation_id=self.conversation_id)

    def play_prev_music(self)->Optional[ResponesMessage]:
        song_message = MemoryServiceUpdate.get_memory_pre_song(session=self.session, 
                                                                conversation_id=self.conversation_id)
        if not song_message:
            return ResponesMessage(message="没有上一首了哦",
                                type=MessageType.PLAY_PREV.value,
                                user = self.user,
                                conversation_id=self.conversation_id)
        
        self.save_chat_history(
            history=HistoryMessage(answer="用户正在听" + song_message.artist + "的" + song_message.song_name)
        )

        return self.get_song_message(mtype=MessageType.PLAY_PREV,
                                     music_list=[song_message])


    def play_next_music(self)->Optional[ResponesMessage]:
        song_message = MemoryServiceUpdate.get_memory_next_song(session=self.session, 
                                                                conversation_id=self.conversation_id)
        if not song_message:
            return ResponesMessage(message="没有下一首了哦",
                                type=MessageType.PLAY_NEXT.value,
                                user = self.user,
                                conversation_id=self.conversation_id)

        self.save_chat_history(
            history=HistoryMessage(answer="用户正在听" + song_message.artist + "的" + song_message.song_name)
        )

        return self.get_song_message(mtype=MessageType.PLAY_NEXT,
                                    music_list=[song_message])
    def qwen_music_chat(self, query:str, prompt:str, history:Optional[str]=None)->Optional[str]:
        messages = [{"role": "system", "content": prompt}]
        if history:
            messages.append({"role": "assistant", "content": history})
        messages.append({"role": "user", "content": query})

        from app import app_config
        return app_config["music_agent"].generate_response(messages)
    

    def qwen_tools_call_chat(self, query:str, prompt:str, history:Optional[str]=None)->Optional[ResponesMessage]:
        messages = self.get_chat_history(query=query,
                                        prompt=prompt,
                                        limit=5)

        messages.insert(1, {"role": "assistant", "content": history}) if history else None

        tools = []
        tools.append(tools_service.get_tools_config("get_the_playlist"))
        tools.append(tools_service.get_tools_config("play_song"))
        tools.append(tools_service.get_tools_config("theme_song"))
        tools.append(tools_service.get_tools_config("recommend"))

        from app import app_config
        tool_resp = app_config["music_agent"].generate_response(messages=messages, tools=tools)
        if not tool_resp.get("tool_calls"):
            return None
        
        tool_resp["tool_calls"][0]["arguments"]["wmusic"] = self
  
        return tools_service.invoke_tools(user=self.user, 
                                        conversation_id=self.conversation_id,
                                        tool_name=tool_resp["tool_calls"][0]["name"], 
                                        tool_parameters=tool_resp["tool_calls"][0]["arguments"])

    def qwen_agent_chat(self, query:str)->Optional[ResponesMessage]:
        if settings.ENABLE_MEM:
            query = mem0_api.get_memories(question=query, 
                                        user_id=self.user)
            logger.debug("get_memories:" + query)

        messages = self.get_chat_history(query=query,
                                        prompt=CHAT_PROMPT)
        tools = []
        if settings.ENABLE_TOOLS:
            tools.append(tools_service.get_tools_config("get_the_playlist"))
            tools.append(tools_service.get_tools_config("play_song"))
            tools.append(tools_service.get_tools_config("theme_song"))
            tools.append(tools_service.get_tools_config("recommend"))

        from app import app_config
        answer = app_config["qwen_agent"].generate_response(messages=messages, tools=tools)
        if not answer:
            return None
        
        if isinstance(answer, dict) and answer.get("tool_calls"):
            answer["tool_calls"][0]["arguments"]["wmusic"] = self
            return tools_service.invoke_tools(user=self.user, 
                                            conversation_id=self.conversation_id,
                                            tool_name=answer["tool_calls"][0]["name"], 
                                            tool_parameters=answer["tool_calls"][0]["arguments"])
        self.save_chat_history(
            history=HistoryMessage(query=query, answer=answer)
        )

        return ResponesMessage(message=answer,
                              user = self.user,
                              type=MessageType.CHATBOT.value, 
                              conversation_id=self.conversation_id)


    def get_chat_history(self, query:str, prompt:str, limit: int=20)->list:
        messages = [{"role": "system", "content": prompt}]

        history_list = MessageServiceUpdate.get_desc_message(session=self.session, 
                                                            conversation_id=self.conversation_id, 
                                                            limit=limit)
        for item in history_list:
            if item.query:
                messages.append({"role": "user", "content": item.query})
            if item.answer:
                messages.append({"role": "assistant", "content": item.answer})

        messages.append({"role": "user", "content": query})

        return messages

    def external_api(self, message: dict)->Optional[ResponesMessage]:
        if not message.get("category"):
            return None

        if message["category"] == BertType.PLAY_MUSIC:#播放歌曲
            return self.get_play_music(message)
        elif message["category"] == BertType.PLAYLIST:#播放歌单
            return self.get_artist_of_playlist_result(message=message)
        elif message["category"] == BertType.LLM_SEARCH:#模糊播放歌曲   
            return self.get_llm_music(message=message)
        elif message["category"] == BertType.PLAY_STORY:#播放故事 1
            return self.get_story_result(message)
        elif message["category"] == BertType.ARTIST_INFO:#查询歌手信息
            return self.get_artist_of_detail_result(message=message)
        elif message["category"] == BertType.LYRIC:#查询歌曲歌词
            return self.get_lyric_of_song(message=message)
        elif message["category"] == BertType.PLAY_PREV:#上一首
            return self.play_prev_music()
        elif message["category"] == BertType.PLAY_NEXT:#下一首
            return self.play_next_music()
        elif message["category"] == BertType.WEATHER:#查询天气
            return self.get_weather_result(message=message)
        ###指令返回
        elif message["category"] == BertType.PAUSE_PLAY:#暂停播放
            return ResponesMessage(conversation_id=self.conversation_id, 
                                   user=self.user, 
                                   type = MessageType.PAUSE_PLAY.value)
        elif message["category"] == BertType.CONTINUE_PLAY: #继续播放
            return ResponesMessage(conversation_id=self.conversation_id, 
                                   user=self.user, 
                                   type = MessageType.CONTINUE_PLAY.value)
        elif message["category"] == BertType.VOLUME_PLUS:#添加音量
            return ResponesMessage(conversation_id=self.conversation_id, 
                                   user=self.user, 
                                   type = MessageType.VOLUME_PLUS.value)
        elif message["category"] == BertType.VOLUME_MINUS: #减低音量
            return ResponesMessage(conversation_id=self.conversation_id, 
                                   user=self.user, 
                                   type = MessageType.VOLUME_MINUS.value)
        elif message["category"] == BertType.SET_VOLUME:#设置音量
            return ResponesMessage(conversation_id=self.conversation_id, 
                                   user=self.user, 
                                   type = MessageType.SET_VOLUME.value)
        elif message["category"] == BertType.VOLUME_MIN:#将音量调到最低
            return ResponesMessage(conversation_id=self.conversation_id, 
                                   user=self.user, 
                                   type = MessageType.VOLUME_MIN.value)
        elif message["category"] == BertType.VOLUME_MAX:#将音量调到最高
            return ResponesMessage(conversation_id=self.conversation_id, 
                                   user=self.user, 
                                   type = MessageType.VOLUME_MAX.value)
        elif message["category"] == BertType.CHATBOT:#模型对话
            return None
        elif message["category"] == BertType.QUERY:#查询历史信息 
            return None
        else:
            return None
        
    async def play_id_music(self, song_id :str)->Optional[ResponesMessage]:
        from app import app_config
        song_detail = app_config["wymusci"].get_song_detail_of_id(song_id)
        if not song_detail:
            logger.error("get get_song_detail error")
            return None
        
        music = MusicMessage.parse_obj(song_detail)

        return self.get_song_message(mtype=MessageType.PLAY_ID_SONG,
                                    music_list=[music])


    def music_agent_chat(self, query:str)->Optional[ResponesMessage]:
        message = bert_categorize(query)
        if not message:
            return self.qwen_agent_chat(query=query)
        
        api_resp = self.external_api(message=message)
        if not api_resp:
            return self.qwen_agent_chat(query=query)
        
        return api_resp
    

async def music_agent_services(session: Session, 
                            user_name:str, 
                            user_query:str, 
                            conversation_id:str)->Optional[ResponesMessage]:
    user_db = UserServiceUpdate.get_user_by_name(session=session, 
                                                 name = user_name)
    if not user_db:
        user_db = UserServiceUpdate.create_user(session=session, 
                                                user_name = user_name)
        if not user_db:
            return {"type": -1, "message": "创建用户失败"}
        
        conversation = ConversationServiceUpdate.create_conversation(session=session, 
                                                                     user_id=user_db.id, 
                                                                     name=user_query) 
        if not conversation:
            return {"type": -1, "message": "创建会问失败"}
    
    if not conversation_id:
        conversation = ConversationServiceUpdate.create_conversation(session=session, 
                                                                     user_id=user_db.id, 
                                                                     name=user_query) 
        if not conversation:         
            return {"type": -1, "message": "创建会问失败"}
    else:
        if not is_valid_uuid(conversation_id):          
            return {"type": -1, "message": "会话ID不合法"}
        
        conversation = ConversationServiceUpdate.get_conversation_by_id(session=session, 
                                                                        conversation_id=conversation_id)
        if not conversation:
            return {"type": -1, "message": "获取会话失败"}

    music_agent = MusicAgent(session=session,
                             user=user_name,
                             conversation_id=str(conversation.id))
    
    return music_agent.music_agent_chat(query=user_query)
