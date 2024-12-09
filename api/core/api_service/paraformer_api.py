import dashscope
import time
import asyncio
from typing import Union
from config.app_config import settings
from dashscope.audio.asr import (Recognition, RecognitionCallback,
                                 RecognitionResult)

dashscope.api_key = settings.QWEN_KEY

class Callback(RecognitionCallback):
    def __init__(self):
        self._data_queue = asyncio.Queue()
        self._is_closed = False
        
    def on_complete(self) -> None:
        self._is_closed = True

    def on_error(self, result: RecognitionResult) -> None:
        self._is_closed = True

    def on_event(self, result: RecognitionResult) -> None:
        # 处理识别结果
        print(result["output"]["sentence"]["text"])
        print(RecognitionResult.is_sentence_end(result))

def get_paraformer_services()->Union[Callback, Recognition]:
    callback = Callback()

    recognition = Recognition(model='paraformer-realtime-v2',
                            format='mp3',
                            sample_rate=16000,
                            callback=callback)
    
    return callback, recognition

# recognition.start()
# recognition.send_audio_frame(chunk)
# recognition.stop()