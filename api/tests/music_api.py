import requests
import json
from typing import Union, Optional
from enum import Enum
from enum import IntEnum

class SearchType(IntEnum):
    ALBUM = 10
    ARTISTS = 100
    SONG     = 1
    PLAYLIST = 1000

  
class MusicRoute(str, Enum):
    SEARCH = "/search"
    ALBUM  = "/album"
    ARTIST_ALBUM = "/artist/album"
    RECOMMEND = "/recommend/songs"
    PERSONAL =  "/personalized/newsong"
    ARTIST_DETAIL = "/artist/detail"
    PLAYLIST      = "/top/playlist/highquality"
    PLAYLIST_SONG ="/playlist/track/all"
    ARTIST_DESC   = "/artist/desc"
    ARTIST_SONGS  = "/artist/songs"
    LYRIC         = "/lyric"
    SONG_URL      = "/song/url/v1"
    SONG_DETAIL   = "/song/detail"
    
class MusicLevel(str, Enum):
    STANDED  = "standard" #标准
    HIGHER   = "higher" #较高
    EXHIGH   = "exhigh"#极高
    LOSSLESS ="lossless"#无损
    HIRES    ="hires"#Hi-Re
    JYEFFECT ="jyeffect"#高清环绕声
    SKY      ="sky" #沉浸环绕声 
    DOLBY    ="dolby" #杜比全景声 
    JYMASTER ="jymaster"#超清母带


class MatchMusic():
    @staticmethod
    def count_same_characters(str1, str2):
        # 找到两个字符串的共同字符
        common_chars = set(str1) & set(str2)

        # 统计每个共同字符在两个字符串中出现的最小次数
        count = 0
        for char in common_chars:
            count += min(str1.count(char), str2.count(char))

        return count
    
    @staticmethod 
    def match_of_artists_name(song_resp: dict, singer_name: str)->Union[None, dict]:
        if not song_resp.get("result",{}).get("songs",[{}])[0].get("artists",[{}])[0].get("name"):
            return None
            
        song_message = {}
        singer_max_number = 0
            
        for item in song_resp["result"]["songs"]:
            artists = "，".join(x["name"] for x in item["artists"])
            match_number = MatchMusic.count_same_characters(singer_name, artists)
            if match_number == len(singer_name):
                song_message["id"]        = item["id"]
                song_message["artists"]   = artists
                song_message["song_name"] = item["name"]
                break
                
            if match_number > singer_max_number:
                singer_max_number = match_number
                song_message["id"]        = item["id"]
                song_message["artists"]   = artists
                song_message["song_name"] = item["name"]

        return song_message if song_message else None
    
    @staticmethod  
    def match_of_song_name(song_resp: dict, song_name:str)->Union[None, dict]:
        if not song_resp.get("result",{}).get("songs",[{}])[0].get("name"):
            return None
            
        song_message = {}
        song_max_number = 0
            
        for item in song_resp["result"]["songs"]:
            artists = "，".join(x["name"] for x in item["artists"])
            match_number = MatchMusic.count_same_characters(song_name, item["name"])
            if match_number == len(song_name):
                song_message["id"]        = item["id"]
                song_message["artists"]   = artists
                song_message["song_name"] = item["name"]
                break
                
            if match_number > song_max_number:
                song_max_number = match_number
                song_message["id"]        = item["id"]
                song_message["artists"]   = artists
                song_message["song_name"] = item["name"]

        return song_message if song_message else None



class MusicApi:
    def __init__(self, url, cookie):
        self.url = url
        self.cookie = cookie
        
    #resp_sjon["result"]["artists"][0]["id"]
    #album_id = resp_sjon.get("result", {}).get("albums", [{}])[0].get("id")
    #聚合搜索
    def search_keyword(self, keywords:str, limit: int, search_type: SearchType)->Union[None, dict]:
        resp = requests.get(url = self.url + MusicRoute.SEARCH, params= {'limit': limit, 'type':  search_type.value, 'keywords' : keywords, "cookie": self.cookie})
        if resp.status_code != 200:
            return None
        
        try:
            resp_sjon = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
            
        return resp_sjon
    
    ## 查询专辑下的歌曲
    def get_album_of_songs(self, album_id: int)->Union[None, list]:
        resp = requests.get(url = self.url + MusicRoute.ALBUM, params = {"id" : album_id, "cookie": self.cookie})
        if resp.status_code != 200:
            return None
        
        try:
            album_sjon = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        song_id = album_sjon.get("songs", [{}])[0].get("id")
        if not song_id:
            return None
        
        play_list = []
        for item in album_sjon["songs"]:
            artists = "，".join(name["name"] for name in item["ar"])
            play_list.append({"name": item["name"], "id": item["id"], "artists":  artists})   
        
        return play_list
    
    ## 查询歌手的所有专辑
    def get_artists_of_albums(self, artist_id:int, limit: int)->Union[None, list]:
        resp  = requests.get(url = self.url  + MusicRoute.ARTIST_ALBUM, params= {"limit": limit, "id" : artist_id, "cookie": self.cookie})
        if resp.status_code != 200:
            return None
        
        try:
            resp_sjon = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        album_id = resp_sjon.get("hotAlbums", [{}])[0].get("id")
        if not album_id:
            return None

        album_list = []
        for item in resp_sjon["hotAlbums"]:
            album_list.append({"name": item["name"], "id": item["id"], "size": item["size"]})   
        
     
        return album_list
    ## 推荐歌曲
    def get_recommend_of_songs(self)->Union[None, list]:
        resp  = requests.get(url = self.url + MusicRoute.RECOMMEND)
        if resp.status_code != 200:
            return None
        
        try:
            resp_sjon = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        song_id = resp_sjon.get("data", {}).get("dailySongs", [{}])[0].get("id")
        if not song_id:
            return None
    
        play_list = []
        for item in resp_sjon["data"]["dailySongs"]:
            artists = "，".join(name["name"] for name in item["ar"])
            play_list.append({"song_name":item["name"], "artist": artists, "song_id":item["id"]})
    
        return play_list
    
    ## 推荐新歌曲
    def get_new_of_songs(self, limit: int)->Union[None, list]:
        resp = requests.get(url = self.url + MusicRoute.PERSONAL, params={"limit" : limit})
        if resp.status_code != 200:
            return None
        
        try:
            resp_sjon = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        song_id = resp_sjon.get("result", [{}])[0].get("id")
        if not song_id:
            return None
        
        play_list = []
        for item in resp_sjon["result"]:
            play_list.append({"song_name":item["name"], "artist":item["song"]["artists"][0]["name"], "song_id":item["id"]})

        return play_list
    
    ## 歌手详细信息
    def get_artist_of_detail(self, artist_id:int)->Optional[str]:
        resp  = requests.get(url = self.url + MusicRoute.ARTIST_DETAIL, params={"id":artist_id, "cookie": self.cookie})
        if resp.status_code != 200:
            return None
        
        try:
            resp_sjon = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        return resp_sjon.get("data", {}).get("artist", {}).get("briefDesc")
    
    ## 搜索高质量歌单
    def get_highquality_of_playlist(self, keywords: str, limit: int)->Union[None, list]:
        resp  = requests.get(url = self.url  + MusicRoute.PLAYLIST, params={"limit" : limit, "cat": keywords, "cookie": self.cookie})
        if resp.status_code != 200:
            return None
        
        try:
            resp_sjon = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        song_id = resp_sjon.get("playlists", [{}])[0].get("id")
        if not song_id:
            return None
        
        play_list = []
        for item in resp_sjon["playlists"]:
            play_list.append({"name":item["name"], "id":item["id"]})

        return play_list
    
    ## 查找歌单中的歌曲
    def get_playlist_of_songs(self, playlist_id:int, limit:int)->Union[None, list]:
        resp  = requests.get(url = self.url  + MusicRoute.PLAYLIST_SONG, params= {"limit":limit, "id": playlist_id, "cookie": self.cookie})
        if resp.status_code != 200:
            return None
        
        try:
            resp_sjon = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        song_id = resp_sjon.get("songs", [{}])[0].get("id")
        if not song_id:
            return None
        
        play_list = []
        for item in resp_sjon["songs"]:
            play_list.append({"name":item["name"], "artists":item["ar"][0]["name"], "id":item["id"]})

        return play_list
    
    ##获取歌手详细信息
    def get_other_artist_of_detail(self, artist_id:int)->Optional[str]:
        resp  = requests.get(url = self.url + MusicRoute.ARTIST_DESC, params={"id":artist_id, "cookie": self.cookie})
        if resp.status_code != 200:
            return None
        
        try:
            resp_sjon = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None

        return resp_sjon.get("briefDesc")
    
    ##获取歌手歌单
    def get_artist_of_playlist(self, artists_id: int, limit: int)->Union[None, list]:
        resp  = requests.get(url = self.url + MusicRoute.ARTIST_SONGS, params={'id': artists_id, 'limit': limit, 'order':"hot", "cookie": self.cookie})
        if resp.status_code != 200:
            return None
        
        try:
            resp_sjon = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        song_id = resp_sjon.get("songs", [{}])[0].get("id")
        if not song_id:
            return None
        
        resp_list = []
        for item in resp_sjon["songs"]:
            resp_list.append({
                "song_id": item["id"], 
                "song_name": item["name"], 
                "artist": item["ar"][0]["name"]
            })
            
        return resp_list
    
    ##获取歌曲的歌词
    def get_song_of_lyrics(self, song_id:int)->Optional[str]:
        resp  = requests.get(url = self.url + MusicRoute.LYRIC, params={"id": song_id, "cookie": self.cookie})
        if resp.status_code != 200:
            return None
        
        try:
            resp_sjon = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        return resp_sjon.get("lrc",{}).get("lyric")
    
    ###获取歌曲的链接
    def get_song_of_url(self, song_id:int, level: str)->str:
        resp  = requests.get(url = self.url + MusicRoute.SONG_URL, params={"id": song_id, "level": level, "cookie": self.cookie}, headers = {"cookie": self.cookie})
        if resp.status_code != 200:
            return None
        
        try:
            resp_sjon = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        return resp_sjon.get("data", [{}])[0].get("url")
    
    ###获取歌曲的ID
    def get_search_match_of_song(self, song_name:str, singer_name: str)->Union[None, dict]:
        song_resp = self.search_keyword(song_name, 30, SearchType.SONG)
        if not song_resp:
            return None

        if not song_resp.get("result",{}).get("songs",[{}])[0].get("id"):
            return None
        
        if singer_name:
            resp = MatchMusic.match_of_artists_name(song_resp, singer_name)
            if resp:
                return resp
        
        resp = MatchMusic.match_of_song_name(song_resp, song_name)
        if resp:
            return resp
        
        return {
            "song_id":      song_resp["result"]["songs"][0]["id"],
            "artist": song_resp["result"]["songs"][0]["artists"][0]["name"],
            "song_name": song_resp["result"]["songs"][0]["name"]
        }
    
    def get_search_of_artist(self, singer_name: str)->Union[None, dict]:
        artists = self.search_keyword(singer_name, 30, SearchType.ARTISTS)
        if not artists:
            return None
        
        if not artists.get("result", {}).get("artists", [{}])[0].get("id"):
            return None
        
        return {
            "id": artists.get("result", {}).get("artists", [{}])[0].get("id"),
            "artist": artists.get("result", {}).get("artists", [{}])[0].get("name"),
        }
    def get_song_detail_of_id(self, song_id: str)->Union[None, dict]: #SONG_DETAIL
        resp  = requests.get(url = self.url + MusicRoute.SONG_DETAIL, params={"ids": song_id, "cookie": self.cookie})
        if resp.status_code != 200:
            return None
        
        try:
            resp_sjon = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        if not resp_sjon.get("songs"):
            return None

        return {
            "id":      resp_sjon["songs"][0]["id"],
            "artists": resp_sjon["songs"][0]["ar"][0]["name"],
            "song_name": resp_sjon["songs"][0]["name"]
        }
    
    ###获取所有的歌曲
    def get_search_song_by_name(self, song_name:str)->Optional[dict]:
        song_resp = self.search_keyword(song_name, 15, SearchType.SONG)
        if not song_resp:
            return None
        
        play_list = []

        for item in song_resp["result"]["songs"]:
            play_list.append({
                "song_id": item["id"],
                "artist" : item["artists"][0]["name"],
                "song_name": item["name"]})
        return play_list