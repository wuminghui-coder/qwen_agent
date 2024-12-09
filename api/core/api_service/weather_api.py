import json
import requests

class weatherApi():
    def __init__(self, key:str):
        self.key = key

    def get_now_weather(self, area: str)->str:
        if not area:
            return None
        
        key      = "key=" + self.key
        location = "&location=" + area
        language = "&language=zh-Hans"
        unit     = "&unit=c"

        resp = requests.get("https://api.seniverse.com/v3/weather/now.json", params = f"{key}{location}{language}{unit}")
        if resp.status_code != 200:
            return None
        
        try:
            resp_sjon = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None

        if not resp_sjon.get("results",[{}])[0].get("location",{}).get("name"):
            return None

        return resp_sjon["results"][0]["location"]["name"] + resp_sjon["results"][0]["now"]["text"] + "，气温" + resp_sjon["results"][0]["now"]["temperature"] + "度"