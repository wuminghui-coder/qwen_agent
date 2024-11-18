from enum import Enum

class BertType(str, Enum):
    #播放歌曲
    PLAY_MUSIC= "PLAY_MUSIC"
    #播放歌单
    PLAYLIST= "PLAYLIST"     
    #模糊播放歌曲
    LLM_SEARCH= "LLM_SEARCH"    
    # 播放故事
    PLAY_STORY= "PLAY_STORY"  
    #查询歌手信息
    ARTIST_INFO= "ARTIST_INFO"        
    #查询歌曲歌词
    LYRIC= "LYRIC"      
    #上一首
    PLAY_PREV= "PLAY_PREV"     
    #下一首
    PLAY_NEXT= "PLAY_NEXT"   
    #模型对话
    CHATBOT = "CHATBOT"     
    #查询天气
    WEATHER = "WEATHER"    
    #查询历史信息
    QUERY = "QUERY"
    #暂停播放
    PAUSE_PLAY= "PAUSE_PLAY"        
    #继续播放
    CONTINUE_PLAY  = "CONTINUE_PLAY"      
    #添加音量
    VOLUME_PLUS= "VOLUME_PLUS"    
    #减低音量
    VOLUME_MINUS= "VOLUME_MINUS"  
    #设置音量
    SET_VOLUME= "SET_VOLUME"       
    #将音量调到最低
    VOLUME_MIN= "VOLUME_MIN"     
    #将音量调到最高
    VOLUME_MAX= "VOLUME_MAX"

class MessageType(int, Enum):  
    #播放歌曲
    PLAY_MUSIC= 0
    #播放歌单
    PLAYLIST= 1    
    #模糊播放歌曲
    LLM_SEARCH= 11    
    # 播放故事
    PLAY_STORY= 13 
    #查询歌手信息
    ARTIST_INFO= 2        
    #查询歌曲歌词
    LYRIC= 3     
    #上一首
    PLAY_PREV= 8     
    #下一首
    PLAY_NEXT= 9   
    #模型对话
    CHATBOT = 10    
    #查询天气
    WEATHER = 12   
    #查询历史信息
    QUERY = 10
    #暂停播放
    PAUSE_PLAY= 6        
    #继续播放
    CONTINUE_PLAY  = 7      
    #添加音量
    VOLUME_PLUS= 4   
    #减低音量
    VOLUME_MINUS= 5 
    #设置音量
    SET_VOLUME= 14       
    #将音量调到最低
    VOLUME_MIN= 16    
    #将音量调到最高
    VOLUME_MAX= 15
    #按ID播放歌曲
    PLAY_ID_SONG=23

class HistoryType(int, Enum): 
    ROBOT_CHAT   = 0
    WEATHER_CHAT = 1
    MUSIC_CHAT   = 2
    CONTROL_CHAT = 3