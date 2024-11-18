from core.api_service.llm import OpenAILLM
from core.api_service.music_api import MusicApi
from core.api_service.ximalaya_api import ximalayaApi
from core.api_service.weather_api import weatherApi
from core.api_service.google_api import GoogleSearch

from core.prompt import MUSIC_PROMPT, CHAT_PROMPT
from config.app_config import settings
import logging
logger = logging.getLogger(__name__)
def init_api(app_config:dict):
    wymusci = MusicApi(url=settings.MUSIC_URL, 
                       cookie=settings.MUSIC_COOKIE)

    ximalaya = ximalayaApi(app_key=settings.XIMALAYA_API_KEY, 
                            app_secret=settings.XIMALAYA_API_SECRET, 
                            base_url=settings.XIMALAYA_API_URL, 
                            sha1Key=settings.XIMALAYA_API_SECRET)

    weather = weatherApi(key=settings.WEATGER_API_KEY)

    google = GoogleSearch(api_key=settings.GOOGLE_KEY, 
                          cse_id=settings.GOOGLE_CSE_ID, 
                          base_url=settings.GOOGLE_URL)
    
    app_config["wymusci"]  = wymusci
    app_config["ximalaya"] = ximalaya
    app_config["weather"] = weather
    app_config["google"] = google