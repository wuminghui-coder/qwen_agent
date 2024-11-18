import requests
import json
from typing import Union, Optional
import logging
logger = logging.getLogger(__name__)

class GoogleSearch:
    def __init__(self, api_key: str, cse_id: str, base_url: str = "https://www.googleapis.com/customsearch/v1"):
        self.api_key = api_key
        self.cse_id = cse_id
        self.base_url = base_url


    def googel_search(self, search_term: str)->Optional[str]:
        params = {
            'q': search_term,           # 搜索关键词
            'key': self.api_key,   # 谷歌搜索API Key
            'cx': self.cse_id,
            "c2coff":0
        }

        response = requests.get(url=self.base_url, params=params)
        if response.status_code != 200:
            return None
        
        try:
            resp = json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        search_resp = resp.get("items")
        if not search_resp:
            return None

        for item in resp["items"]:
            firecrawl_resp = self.firecrawl_post(item["link"])
            if firecrawl_resp:
                break

        return firecrawl_resp
      

    def firecrawl_post(self, url: str)->Optional[str]:
        header = {
            "Content-Type": "application/json"
        }

        body = {
            "url":url,
        }
   
        response = requests.post(url="http://localhost:3002/v0/scrape", data=json.dumps(body), headers=header)
        if response.status_code != 200:
            return None
        
        try:
            resp = json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        logger.debug(resp["data"]["content"])

        return resp["data"]["content"]
    
        