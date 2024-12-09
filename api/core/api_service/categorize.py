
import requests
import json
from typing import Union,Optional
import logging

logger = logging.getLogger(__name__)
def bert_https_request(query:str)->Optional[str]:
    headers = {
        "Content-Type": "application/json",
        "accept":"application/json"
    }

    resp = requests.post(url= "http://172.30.13.207:8036/detect_intent", headers=headers, data= json.dumps({"text":query}))
    if resp.status_code != 200:
        return None
    
    try:
        resp_json = json.loads(resp.text)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None
    
    return resp_json

def bert_categorize(query:str)->Optional[str]:
    resp = bert_https_request(query)
    if not resp:
        logger.error("get bert_categorize error")
        return None, None

    message = {}

    if resp.get('slots'):
        slot = resp.get('slots')
        if slot.get("artist"):
            message["artist"] = slot.get("artist", [])[0]

        if slot.get("song"):
            song_name = ",".join(x for x in slot.get("song"))
            message["song_name"] = song_name

        if slot.get("name"):
            song_name = ",".join(x for x in slot.get("name"))
            message["song_name"] = song_name

        if slot.get("location_city"):
            message["weather"] = slot.get("location_city", [])[0]

        if slot.get("value"):
            message["value"] = slot.get("value", [])[0]

    if resp.get("intent"):
        message["category"] = resp.get("intent")

    message["query"] = query
    logger.debug(message)
    return message

