import dashscope
from dashscope.audio.tts_v2 import *
import asyncio
from typing import Union
from config.app_config import settings

dashscope.api_key = settings.QWEN_KEY

class Callback(ResultCallback):
    def __init__(self):
        self._data_queue = asyncio.Queue()
        self._is_closed = False

    # def on_open(self):
    #     print("websocket is open.")

    def on_complete(self):
        #print("speech synthesis task complete successfully.")
        self._is_closed = True

    def on_error(self, message: str):
        #print(f"speech synthesis task failed, {message}")
        self._is_closed = True

    def on_close(self):
        #print("websocket is closed.")
        self._is_closed = True

    # def on_event(self, message):
    #     print(f"recv speech synthesis message {message}")

    def on_data(self, data: bytes) -> None:
        #print("audio result length:", len(data))
        self._data_queue.put_nowait(data)

    async def stream_audio(self):
        while not self._is_closed or not self._data_queue.empty():
            data = await self._data_queue.get()
            yield data

def get_audio_service(voice:str)->Union[Callback, SpeechSynthesizer]:
    callback = Callback()

    synthesizer = SpeechSynthesizer(
        model="cosyvoice-v1",
        voice=voice,
        callback=callback,
        format=AudioFormat.DEFAULT
    )

    return callback, synthesizer