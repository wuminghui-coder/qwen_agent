import logging
import re
from core.api_service.music_api import MusicLevel
from core.prompt import MUSIC_PROMPT
from core.api_service.categorize import bert_categorize
from typing import Union
from fields.message_type import MessageType, BertType
from core.prompt import MUSIC_PROMPT, CHAT_PROMPT
from core import crud
import time
logger = logging.getLogger(__name__)
from extensions.exten_sql import SessionDep

def play_id_song(artist:str, song_name:str, song_id:int, mtype:MessageType)->Union[None, dict]:
    from app import app_config

    song_url = app_config["wymusci"].get_song_of_url(song_id, MusicLevel.LOSSLESS)
    if not song_url:
        logger.error(f"Get song of url failed: {song_id}")
        return None

    song_lyric = app_config["wymusci"].get_song_of_lyrics(song_id)
    if not song_lyric:
        logger.error(f"Get song of lyrics failed: {song_id}")
        return None

    return {
        "result"     : song_url,
        "lyric"      : song_lyric,
        "code"       : 200,
        "type"       : mtype.value, 
        "artist"     : artist,
        "song_name"  : song_name.replace("《", "").replace("》", ""),
        "message"    : "好的，正在播放" + artist + "的《" + song_name + "》"  ,
        "song_id"    : song_id
    }

def get_song_result(song_name:str, artist:str)->Union[None, dict]:
    song_name = song_name.replace("《", "").replace("》", "")

    from app import app_config
    resp = app_config["wymusci"].get_search_match_of_song(song_name, artist)
    if not resp:
        return None

    return play_id_song(resp["artists"], resp["song_name"], resp["id"], MessageType.PLAY_MUSIC)


def id_get_song_result(artist:str)->Union[None, dict]:
    from app import app_config
    artist_resp = app_config["wymusci"].get_search_of_artist(artist)
    if not artist_resp:
        return None
        
    song_list = app_config["wymusci"].get_artist_of_playlist(artist_resp["id"], 20)
    if not song_list:
        return None

    resp = play_id_song(song_list[0]["artist"], song_list[0]["name"], song_list[0]["id"], MessageType.LLM_SEARCH)
    if not resp:
        return None
    
    resp["song_list"] = song_list

    return resp


def id_get_lyric_result(session: SessionDep, conversation_id:str, message: dict)->Union[None, dict]:
    if not message.get("song_name"):
        return None

    song_name = message.get("song_name")
    song_name = song_name.replace("《", "").replace("》", "")
    from app import app_config
    resp = app_config["wymusci"].get_search_match_of_song(song_name, None)
    if not resp:
        return None

    song_lyric = app_config["wymusci"].get_song_of_lyrics(resp["id"])
    if not song_lyric:
        return None
    
    song_lyric = re.sub(r'\[.*?\]', '', song_lyric)
    song_lyric = song_lyric.replace('\n', '，').strip()

    return {
        "code"       : 200,
        "type"       : MessageType.LYRIC.value,
        "message"    : "好的，" + resp["song_name"] + "的歌词是：" + song_lyric,
        "song_name"  : resp["song_name"]
    }


def get_artist_of_playlist_result(session: SessionDep, conversation_id:str, message: dict)->Union[None, dict]:
    if not message.get("artist"):
        return None
        
    from app import app_config
    artist_resp = app_config["wymusci"].get_search_of_artist(message.get("artist"))
    if not artist_resp:
        return None
        
    song_list = app_config["wymusci"].get_artist_of_playlist(artist_resp["id"], 20)
    if not song_list:
        return None
    
    songlist = "，".join(x["name"] for x in song_list)

    return {
        "song_list"   : song_list,
        "code"        : 200,
        "type"        : MessageType.PLAYLIST,
        "message"     :"好的，" + artist_resp["artist"] + "的歌曲有" + songlist,
        "artist"      : artist_resp["artist"]
    }

def get_artist_of_detail_result(session: SessionDep, conversation_id:str, message: dict)->Union[None, dict]:
    if not message.get("artist"):
        return None

    from app import app_config
    artist_resp = app_config["wymusci"].get_search_of_artist(message.get("artist"))
    if not artist_resp:
        return None
        
    artist_detail = app_config["wymusci"].get_other_artist_of_detail(artist_resp["id"])
    if not artist_detail:
        return None
    
    return {
        "code"        : 200,
        "type"        : MessageType.ARTIST_INFO.value,
        "message"     :"好的，" + artist_detail,
        "artist"      : message.get("artist")
    }

def qwen_music_chat(query:str)->Union[None, str]:
    messages = [
        {"role": "system", "content": MUSIC_PROMPT},
        {"role": "user", "content": query},
    ]
    from app import app_config
    return app_config["music_agent"].generate_response(messages)


def play_music(message: dict)->Union[None, dict]:
    if not message.get("artist") and not message.get("song_name"):
        song_name = qwen_music_chat(message.get("query"))
        return get_song_result(song_name, None)
    elif message.get("artist") and not message.get("song_name"):
        return id_get_song_result(message.get("artist"))
    elif message.get("artist") and message.get("song_name"):
        return get_song_result(message.get("song_name"), message.get("artist"))
    elif not message.get("artist") and message.get("song_name"):
        return get_song_result(message.get("song_name"), None)
    else:
        song_name = qwen_music_chat(message.get("query"))
        return get_song_result(song_name, None)


async def play_id_music(song_id :str)->dict:
    from app import app_config
    
    song_detail = app_config["wymusci"].get_song_detail_of_id(song_id)
    if not song_detail:
        return None
    
    return play_id_song(song_detail["artists"], song_detail["song_name"], song_id, MessageType.PLAY_ID_SONG)

def play_stop_music()->dict:
    return {
        "message": "好的", 
        "type": MessageType.PAUSE_PLAY.value, 
    }

def play_contiune_music()->dict:
    return {
        "message": "好的", 
        "type": MessageType.CONTINUE_PLAY.value, 
    }

def play_volume_plus_music()->dict:
    return {
        "message": "好的", 
        "type": MessageType.VOLUME_PLUS.value, 
    }

def play_volume_minus_music()->dict:
    return {
        "message": "好的", 
        "type": MessageType.VOLUME_MINUS.value, 
    }

def play_set_volume_music(message:dict)->dict:
    if not message.get("value"):
        return None
    
    return {
        "message": "好的", 
        "type": MessageType.SET_VOLUME.value, 
        "value": message.get("value")
    }

def play_max_volume_music()->dict:
    return {
        "message": "好的", 
        "type": MessageType.VOLUME_MAX.value, 
    }

def play_min_volume_music()->dict:
    return {
        "message": "好的", 
        "type": MessageType.VOLUME_MIN.value, 
    }


def get_chat_history(session: SessionDep, conversation_id:str, query:str)->list:
    messages = []
    messages.append({"role": "system", "content": CHAT_PROMPT})

    history_list = crud.get_desc_message(session=session, 
                                         conversation_id=conversation_id, 
                                         limit=20)

    for item in history_list:
        messages.append({"role": "user", "content": item.query})
        messages.append({"role": "assistant", "content": item.answer})

    messages.append({"role": "user", "content": query})

    return messages


def save_chat_history(session: SessionDep, 
                      conversation_id:str, 
                      query:str, 
                      answer:str):
    history = {
        "query":query,
        'answer': answer,
        'answer_tokens':len(answer),
        'error': BertType.CHATBOT.value,
    }

    new_message = crud.create_message(session=session, 
                                      conversation_id=conversation_id, 
                                      args=history)
    if not new_message:
        return {"type": -1, "message": "创建消息失败"}


def qwen_agent_chat(session: SessionDep, conversation_id:str, query:str)->dict: 
    from app import app_config
    if not app_config.get("qwen_agent"):
        return None
    
    messages = get_chat_history(session=session, 
                                conversation_id=conversation_id, 
                                query=query)

    answer = app_config["qwen_agent"].generate_response(messages)
    if not answer:
        return {"type": -1, "message": "对话模型返回为空"}

    save_chat_history(session=session, 
                      conversation_id=conversation_id, 
                      query=query,
                      answer=answer)
    return {
        "message": answer,
        "type": MessageType.CHATBOT.value
    }

def get_story_result(message: dict)->Union[None, dict]:
    if not message.get("song_name"):
        return None
    
    from app import app_config
    resp = app_config["ximalaya"].get_search_tracks(message.get("song_name"))
    if not resp:
        return None
    
    return {
        "message" : "好的，正在播放故事《" + resp[0]["track_title"] + "》",
        "type"    :  MessageType.PLAY_STORY.value,
        "result"  :  resp[0]['play_url'],
    }

def get_weather_result(message: dict)->Union[None, dict]:
    if not message.get("weather"):
        return None
    
    from app import app_config
    resp = app_config["weather"].get_now_weather(message.get("weather"))
    if not resp:
        return None
  
    return {
        "message" : resp,
        "type"    : MessageType.WEATHER.value,
    }


def external_api(session: SessionDep, conversation_id:str, message: dict)->Union[None, dict]:
    if not message.get("category"):
        return None
    
    if message["category"] == BertType.PLAY_MUSIC:#播放歌曲
        return play_music(message)
    elif message["category"] == BertType.PLAYLIST:#播放歌单
        return get_artist_of_playlist_result(session=session, conversation_id=conversation_id, message=message)
    elif message["category"] == BertType.LLM_SEARCH:#模糊播放歌曲 
        song_name = qwen_music_chat(message["query"])
        return get_song_result(song_name, None)
    elif message["category"] == BertType.PLAY_STORY:#播放故事 1
        return get_story_result(message)
    elif message["category"] == BertType.ARTIST_INFO:#查询歌手信息
        return get_artist_of_detail_result(session=session, conversation_id=conversation_id, message=message)
    elif message["category"] == BertType.LYRIC:#查询歌曲歌词
        return id_get_lyric_result(session=session, conversation_id=conversation_id, message=message)
    elif message["category"] == BertType.PLAY_PREV:#上一首
        return None
        #return  play_prev_music(session=session, conversation_id=conversation_id)
    elif message["category"] == BertType.PLAY_NEXT:#下一首
        return None
        #return  play_next_music(session=session, conversation_id=conversation_id)
    elif message["category"] == BertType.CHATBOT:#模型对话
        return None
    elif message["category"] == BertType.WEATHER:#查询天气
        return get_weather_result(message)
    elif message["category"] == BertType.QUERY:#查询历史信息 
        return None
    elif message["category"] == BertType.PAUSE_PLAY:#暂停播放
        return play_stop_music()
    elif message["category"] == BertType.CONTINUE_PLAY: #继续播放
        return play_contiune_music()
    elif message["category"] == BertType.VOLUME_PLUS:#添加音量
        return play_volume_plus_music()
    elif message["category"] == BertType.VOLUME_MINUS: #减低音量
        return play_volume_minus_music()
    elif message["category"] == BertType.SET_VOLUME:#设置音量
        return play_set_volume_music(message)
    elif message["category"] == BertType.VOLUME_MIN:#将音量调到最低
        return play_min_volume_music()
    elif message["category"] == BertType.VOLUME_MAX:#将音量调到最高
        return play_max_volume_music()
    else:
        return None

def time_consume(describe: str, timestamp:int):
    current_timestamp1 = int(time.time() * 1000) - timestamp
    logger.debug( f"{describe} 耗时：{current_timestamp1}ms")

def model_dialogue(session: SessionDep, 
               conversation_id:str, 
               query:str)->Union[None, dict]:
    
    timestamp = int(time.time() * 1000)
    agent_resp = qwen_agent_chat(session=session, 
                                conversation_id=conversation_id,
                                query=query)
    time_consume("阿里千问7b", timestamp)

    return agent_resp

def external_api_service(session: SessionDep, 
                         conversation_id:str, 
                         query:str)->Union[None, dict]:
    
    timestamp = int(time.time() * 1000)
    message = bert_categorize(query)
    time_consume("意图识别", timestamp)
    if not message:
        return None 
     
    timestamp = int(time.time() * 1000)

    external_api_resp = external_api(session=session, 
                                    conversation_id=conversation_id, 
                                    message = message)
    time_consume("外部服务API", timestamp)
    return external_api_resp

async def agent_chat(session: SessionDep, 
               conversation_id:str, 
               query:str)->Union[None, dict]:
    
    api_resp = external_api_service(session=session, 
                            conversation_id=conversation_id, 
                            query=query)
    if not api_resp:
        return model_dialogue(session=session, 
                             conversation_id=conversation_id, 
                             query=query)
    return api_resp



