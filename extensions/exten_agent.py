from core.api_service.llm import OpenAILLM
from core.api_service.music_api import MusicApi
from core.api_service.ximalaya_api import ximalayaApi
from core.api_service.weather_api import weatherApi
from core.prompt import MUSIC_PROMPT, CHAT_PROMPT
from config.app_config import settings

def init_agent(app_config:dict):

    if settings.OPENAI_ENABLE:
        qwen_agent = OpenAILLM(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_KEY,
            base_url=settings.OPENAI_URL,
            temperature=0.8,
            top_p=0.9,
            max_tokens=settings.OPENAI_MAX_TOKEN,
        )
    else:
        qwen_agent = OpenAILLM(
            model=settings.QWEN_MODEL,
            api_key=settings.QWEN_KEY,
            base_url=settings.QWEN_URL,
            temperature=0.8,
            top_p=0.9,
            max_tokens=settings.QWEN_MAX_TOKEN,
        )

    music_agent = OpenAILLM(
        model=settings.QWEN_MODEL,
        api_key=settings.QWEN_KEY,
        base_url=settings.QWEN_URL,
        temperature=0.8,
        top_p=0.9,
        max_tokens=settings.QWEN_MAX_TOKEN,
    )

    app_config["qwen_agent"]  = qwen_agent
    app_config["music_agent"] = music_agent
