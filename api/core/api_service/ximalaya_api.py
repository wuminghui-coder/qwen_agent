import requests
import time
import base64
from urllib.parse import urlencode
import hmac
import hashlib
import json
import uuid
import netifaces
from typing import Union,Optional
from enum import Enum


def get_mac_address(interface):
    try:
        addresses = netifaces.ifaddresses(interface)
        mac = addresses[netifaces.AF_LINK][0]['addr']
        return mac
    except KeyError:
        return None
    
class XimalayaRoute(str, Enum):
    CATEGORIES     = "/categories/list"
    SEARCH_ALBUM   = "/search/albums"
    SEARCH_ALL     = "/search/all"
    SEARCH_TRACKS  = "/search/tracks"
    TAGS_LIST      = "/v2/tags/list"
    ALBUN_LIST     = "/v2/albums/list"
    ALBUM_BROWSE   = "/albums/browse"
    METADATA_ALBUM = "/v2/metadata/albums"
    METADATA_LIST  =  "/v2/metadata/list"

class ximalayaApi:
    def __init__(self, app_key:str, app_secret:str, base_url:str, sha1Key:str):
        self.app_key    = app_key
        self.app_secret = app_secret
        self.base_url   = base_url
        self.sha1Key    = sha1Key
    
    def ximalaya_http_requests(self, url: str, send_message:dict)->Optional[str]:
        timestamp = time.time()
        send_message["device_id"]             = get_mac_address('eth0')
        send_message["device_id_type"]        = "UUID"
        send_message["app_key"]               = self.app_key
        send_message["client_os_type"]        = 3
        send_message["nonce"]                 = "d15d792875807b0fec620f4db2ac1667"
        send_message["timestamp"]             = int(timestamp* 1000)
        
        ### key排序
        sorted_dict = dict(sorted(send_message.items()))

        ### 拼接
        query_string = urlencode(sorted_dict, quote_via=lambda x, *_: x)

        ### base64编码
        byte_data = query_string.encode('utf-8')
        encoded_data = base64.b64encode(byte_data)

        ### hmac编码
        hmac_object = hmac.new(self.sha1Key.encode('utf-8'), encoded_data , hashlib.sha1)
        hmac_result = hmac_object.digest()
        
        ### md5值
        md5 = hashlib.md5()
        md5.update(hmac_result)
        md5_hash = md5.hexdigest()

        send_message["sig"] = md5_hash

        resp = requests.get(url = self.base_url + url, params=send_message, headers = {"Content-Type":"application/json;charset=UTF-8"})
        if resp.status_code != 200:
            return None
        
        try:
            resp_json = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        return resp_json


    #分类列表
    def get_categories_list(self)->Union[None, list]:
        resp = self.ximalaya_http_requests(XimalayaRoute.CATEGORIES, send_message={})
        if not resp:
            return None
        
        sorted_data = sorted(resp, key=lambda item: item['id'])
        
        categories_list = []
        for item in sorted_data:
            categories_list.append({"id":item["id"], "category_name":item["category_name"]})

        return categories_list


    #声音搜索专辑
    def get_search_albums(self, search: str)->Union[None, list]:
        send_message={}
        send_message["q"]               = search
        send_message["category_id"]     = -1    #分类ID。分类数据可以通过 
        #send_message["calc_dimension"] = 1    #1-最火，2-最新，3-最多播放
        #send_message["page"]           = 1
        #send_message["count"]          = 20
        send_message["contains_paid"]  = False 
        # 返回值是否需要包含付费内容：true-包含，false-不包含。默认为false
        
        resp_json = self.ximalaya_http_requests(XimalayaRoute.SEARCH_ALBUM, send_message)
        if not resp_json:
            return None
        
        #json_string = json.dumps(resp_json , indent=4, separators=(',', ': '))

        album_list = []
        for item in resp_json["albums"]:
            album_list.append({"id":item["id"],"album_title": item["album_title"], "album_intro" : item["album_intro"]})

        return album_list



    def get_search_albums_all(self, search: str)->Union[None, list]:
        send_message={}
        send_message["q"]              = search
        #send_message["page"]           = 1
        #send_message["count"]          = 20
        send_message["contains_paid"]  = False 
        # 返回值是否需要包含付费内容：true-包含，false-不包含。默认为false
        
        resp_json = self.ximalaya_http_requests(XimalayaRoute.SEARCH_ALL, send_message)
        if not resp_json:
            return None
        
        #json_string = json.dumps(resp_json , indent=4, separators=(',', ': '), ensure_ascii=False)
        
        album_list = []
        for item in resp_json["album_list"]["albums"]:
            album_list.append({"id":item["id"],"album_title": item["album_title"], "album_intro" : item["album_intro"]})
        
        tracks_list = []
        for item in resp_json["track_list"]["tracks"]:
            print(item["id"], item["track_title"], item["track_tags"], item["play_url_32"])
            tracks_list.append({
                "id": item["id"], 
                "track_title":item["track_title"], 
                "track_tags":item["track_tags"],          
                "play_url_32":item["play_url_32"]
            })

        return album_list, tracks_list


    #声音搜索声音
    def get_search_tracks(self, search: str)->Union[None, list]:
        send_message={}
        send_message["q"]              = search
        send_message["category_id"]    = -1 #分类ID。分类数据可以通过 
        send_message["calc_dimension"] = 1    #1-最火，2-最新，3-最多播放
        send_message["page"]           = "1"
        send_message["count"]          = "20"
        send_message["contains_paid"]  = False # 返回值是否需要包含付费内容：true-包含，false-不包含。默认为false

        resp = self.ximalaya_http_requests(XimalayaRoute.SEARCH_TRACKS, send_message)
        if not resp:
            return None
        
        #json_string = json.dumps(resp , indent=4, separators=(',', ': '))
        tracks_list = []
        for item in resp["tracks"]:
            tracks_list.append({"song_id":item["id"], 
                                "song_url": item["play_url_32"], 
                                "song_name":item["track_title"],
                                "artist":item["subordinated_album"]["album_title"],
                                "image":item["cover_url_small"]})

        return tracks_list


    #热词搜索
    def get_search_hot_words(self, search: str):
        send_message={}
        send_message["top"]              = search  #获取前top长度的热搜词。（1<=top<=20：目前top只支持最多20个）
        send_message["category_id"]      = 0    #分类ID。分类数据可以通过 
        url="https://api.ximalaya.com/search/hot_words"
        resp = self.ximalaya_http_requests(url, send_message)
        if not resp:
            return None
        

    #推荐词搜索
    def get_search_suggest_words(self, search: str):
        send_message={}
        send_message["q"]              = search
        url="https://api.ximalaya.com/search/suggest_words"
        resp = self.ximalaya_http_requests(url, send_message)
        #json_string = json.dumps(resp , indent=4, separators=(',', ': '))
        #print(resp)


    #获取猜你喜欢的专辑信息
    def get_guess_like_albums(self):
        send_message={}
        send_message["device_type"]  = 3  #系统类型： 1-IOS，2-Android，3-Web，4-Linux，5-ecos，6-qnix
        send_message["like_count"]   = 20  #返回几条结果数据，默认为3，取值区间为[1,50]
        #send_message["show_type"]   =    #内容推荐展示效果类型，默认值为2，取值为1、2、3 ; 1--若用户行为（搜索、播放等）没有变化的情况下，返回的专辑内容一样；2--基于专辑评分Top20的内容加入轮循规则; 3--基于用户浏览过的专辑进行过滤后再展示；
        send_message["category_id"] =  0  #专辑分类ID，为0时表示热门分类；支持传一个或多个专辑分类，多个专辑分类ID用‘英文逗号’拼接，如‘0,1,2’；分类数据可以通过categories/list 获取

        url="https://api.ximalaya.com/v2/albums/guess_like"
        resp = self.ximalaya_http_requests(url, send_message)
        #json_string = json.dumps(resp , indent=4, separators=(',', ': '))
        #for item in resp:
        #    print(item["id"], item["album_title"])
        #print(json_string)


    #获取某个专辑的相关专辑信息
    def get_relative_albums(self, album_id:str):
        send_message={}
        send_message["album_id"]  = album_id       #系统类型： 1-IOS，2-Android，3-Web，4-Linux，5-ecos，6-qnix
        #send_message["contains_paid"]  = 4  #返回值是否需要包含付费内容：true-包含，false-不包含。默认为false
        url="https://api.ximalaya.com/v2/albums/relative_albums"
        resp = self.ximalaya_http_requests(url, send_message)
        #print(resp)

    #二级标签列表
    def get_tag_list(self, category_id: int)->Union[None, list]:
        send_message={}
        send_message["category_id"]  = category_id        
        send_message["type"]         = 0
        #send_message["type"] type 指定返回专辑标签还是声音标签：0-专辑标签
        resp_json   = self.ximalaya_http_requests(XimalayaRoute.TAGS_LIST, send_message)
        if not resp_json:
            return None
        
        #json_string = json.dumps(resp_json , indent=4, separators=(',', ': '), ensure_ascii=False)
        #print(json_string)

        tag_list = []
        for item in resp_json:
            tag_list.append(item["tag_name"])

        return tag_list


    #专辑列表
    def get_albums_list(self, category_id: int, tag_name: str):
        send_message={}
        send_message["category_id"]       = category_id
        send_message["tag_name"]          = tag_name
        send_message["calc_dimension"]    = 1 #1-最火，2-最新，3-最多播放
        send_message["page"]              = "1"
        send_message["count"]             = "20"
        send_message["contains_paid"]     = False # 返回值是否需要包含付费内容：true-包含，false-不包含。默认为false

        resp = self.ximalaya_http_requests(XimalayaRoute.ALBUN_LIST, send_message)
        if not resp:
            return None
        
        album_list = []
        for item in resp["albums"]:
            album_list.append({
                                "id":item["id"], 
                                "category_id":item["category_id"] ,
                                "album_title":item["album_title"], 
                                "can_download":item["can_download"],
                                "album_tags" : item["album_tags"]
                            })
        
        return album_list

    #获取专辑下的声音列表
    def get_albums_browse(self, album_id:int)->Union[None, list]:
        send_message={}
        send_message["album_id"]       = album_id      
        send_message["sort"]           = "asc" #返回结果排序方式： 默认为"asc"
        send_message["page"]           = "1"
        send_message["count"]          = "20"

        resp = self.ximalaya_http_requests(XimalayaRoute.ALBUM_BROWSE, send_message)
        if not resp:
            return None
        #json_string = json.dumps(resp , indent=4, separators=(',', ': '), ensure_ascii=False)
        tracks_list = []
        for item in resp["tracks"]:
            #tracks_list.append({"id":item["id"], "play_url_32" : item["play_url_32"], "track_title":item["track_title"]})
            tracks_list.append({"song_id":item["id"], 
                                "song_url": item["play_url_32"], 
                                "song_name":item["track_title"],
                                "artist":item["subordinated_album"]["album_title"],
                                "image":item["cover_url_small"]})

        return tracks_list

    #批量获取专辑信息
    def get_albums_batch(self):
        send_message={}
        send_message["ids"]            = "71396165"     #以英文逗号分隔的专辑ID，一次最多传100个，超出部分ID会被忽略   
        #send_message["with_metadat"]   = False           #true代表返回metadata，false或不填不返回，获取所有元数据列表
        url="https://api.ximalaya.com/albums/get_batch"
        resp = self.ximalaya_http_requests(url, send_message)
        print(resp)

    #批量获取专辑更新信息
    def get_update_batch(self):
        send_message={}
        send_message["ids"]            = "47412394"     #以英文逗号分隔的专辑ID，一次最多传100个，超出部分ID会被忽略   
        url="https://api.ximalaya.com/albums/get_update_batch"
        self.ximalaya_http_requests(url, send_message)


    #获取单个声音信息
    def get_single(self):
        send_message={}
        send_message["track_id"]            = "574574181"    #声音ID。可使用声音ID：19586586 进行调试
        send_message["only_play_info"]      = True           #可选参数，为true时只返回音频播放地址
        url="https://api.ximalaya.com/tracks/get_single"
        resp = self.ximalaya_http_requests(url, send_message)
        print(resp)


    #批量获取声音信息
    def get_update_single(self):
        send_message={}
        send_message["ids"]                 = "19586586"    #声音ID。可使用声音ID：19586586 进行调试
        send_message["only_play_info"]      = True           #可选参数，为true时只返回音频播放地址
        url="https://api.ximalaya.com/tracks/get_batch"
        self.ximalaya_http_requests(url, send_message)

    #获取某条声音在专辑内所属声音页信息列表
    def get_last_play_tracks(self):
        send_message={}
        send_message["album_id"]      = "19586586"    #该声音所属专辑ID   
        send_message["track_id"]      = "19586586"    #声音ID     
        send_message["count"]         = 20            #每页大小，范围为[1,100]，默认为20 

        send_message["sort"]          = "asc"         #正序取页结果或倒序取页结果："asc" - 正序，"desc" - 倒序，默认为"asc
        send_message["contains_paid"] = False         #是否输出付费内容（即返回值是否包含付费内容）：true-是；false-否；默认不填为false
    
        url="https://api.ximalaya.com/tracks/get_last_play_tracks"
        self.ximalaya_http_requests(url, send_message)

    #比量获取声音播放地址信息
    def get_last_play_tracks(self):
        send_message={}
        send_message["ids"]                 = "47412394"    #声音ID。可使用声音ID：19586586 进行调试
        send_message["device_id"]           = "32cc6f279c7a11e9a26e0235d2b38928"
        send_message["device_id_type"]      =  "OAID"

        url="https://api.ximalaya.com/openapi_play_url/tracks/batch_get_play_info"
        self.ximalaya_http_requests(url, send_message)

    #获取某个分类下的元数据列表
    def get_metadata(self, category_id:int)->Union[None, list]:
        resp_json = self.ximalaya_http_requests(XimalayaRoute.METADATA_LIST, send_message = {"category_id" : category_id})
        if not resp_json:
            return None
        
        for item0 in resp_json:
            for item in item0["attributes"]:
                self.get_metadata_albums(id, str(item["attr_key"]) + ":" + item["attr_value"])
                print(item["attr_value"] + str(item["attr_key"]))
                if "child_metadatas" in item:
                    for item1 in item["child_metadatas"]:
                        for item2 in item1["attributes"]:
                            print("    " +  item2["attr_value"] + str(item2["attr_key"]))
                            if "child_metadatas" in item2:
                                for item3 in item2["child_metadatas"]:
                                    for item4 in item3["attributes"]:
                                        print("        " + item4["attr_value"] + str(item4["attr_key"]))
                                        if "child_metadatas" in item4:
                                            for item5 in item4["child_metadatas"]:
                                                for item6 in item5["attributes"]:
                                                    print("            " + item6["attr_value"] + str(item6["attr_key"]))
        #json_string = json.dumps(resp_json , indent=4, separators=(',', ': '), ensure_ascii=False)                                    
        #print(json_string)

    #获取某元数据下的专辑列表
    def get_metadata_albums(self, category_id:int, arg:str)->Union[None, list]:
        send_message={}
        send_message["category_id"]         = category_id
        send_message["metadata_attributes"] = arg 
        #元数据属性列表：/metadata/list接口得到的结果中，
        #取不同元数据属性的attrkey和atrrvalue组成任意个数的key-value键值，注意： 此字段可为空，为空表示获取此分类下全部的最火、最新或者播放最多的专辑列表
        send_message["calc_dimension"] = 1    #1-最火，2-最新，3-最多播放
        send_message["page"]           = "1"
        send_message["count"]          = "30"   
        resp_json = self.ximalaya_http_requests(XimalayaRoute.METADATA_ALBUM, send_message)
        if not resp_json:
            return None
        
        albums_list = []
        for item in resp_json["albums"]:
            print(item["id"], item["album_title"], item["meta"], item["can_download"])
            albums_list.append({
                "id":item["id"], 
                "album_title":item["album_title"], 
                "meta":item["meta"], 
                "can_download":item["can_download"]
            })
        #json_string = json.dumps(resp_json , indent=4, separators=(',', ': '), ensure_ascii=False)
        #print(json_string)
        return albums_list


    def get_albums_story(self, query:str)->Optional[list]:
        album_list = self.get_search_albums(query)
        if not album_list:
            return None
        
        return self.get_albums_browse(album_list[0]['id'])

def ximalaya_test():
    app_key  ="3e0eb29c4d37481587aa7dc94d0fc77b"
    appSecret="31B69473EF89EA4C8E9E27847952B47A"
    base_url="https://api.ximalaya.com/ximalayaos-openapi-xm"

    ximalaya = ximalayaApi(app_key, appSecret, base_url, appSecret)
    resp = ximalaya.get_categories_list()
    for item in resp:
        print(item)

    resp = ximalaya.get_tag_list(6)
    for item in resp:
        print(item)

    resp = ximalaya.get_search_albums("郭德纲")
    for item in resp:
        print(item)

    resp = ximalaya.get_albums_browse(13185100)
    for item in resp:
        print(item)

    resp = ximalaya.get_albums_list(6, "动物乐园")
    for item in resp:
        print(item)

    resp = ximalaya.get_search_tracks("郭德纲")
    for item in resp:
        print(item)

    resp,resp1 = ximalaya.get_search_albums_all("郭德纲")
    for item in resp:
        print(item)
    for item in resp1:
        print(item)

    ximalaya.get_metadata(1)







