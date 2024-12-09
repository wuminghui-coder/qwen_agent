#import pyaudio
import dashscope
import time
import json
import dashscope
from dashscope.audio.asr import *
from dashscope.audio.asr import (Recognition, RecognitionCallback,VocabularyService,
                                 RecognitionResult)

dashscope.api_key = "sk-d4a24c9626034f5384a68490f983f97b"

class Callback(RecognitionCallback):
    def on_complete(self) -> None:
        # 识别完成
        print("on_complet")

    def on_error(self, result: RecognitionResult) -> None:
        # 错误处理
        print(result)

    def on_event(self, result: RecognitionResult) -> None:
        # 处理识别结果
        print(result["output"]["sentence"]["text"])
        print(RecognitionResult.is_sentence_end(result["output"]["sentence"]))
        #resp_json = json.loads(result)
        #json_string = json.dumps(result , indent=4, separators=(',', ': '), ensure_ascii=False)
        #print(json_string)
        #print(result["output"])

my_vocabulary = [
    {"text": "吴贻弓", "weight": 4, "lang": "zh"},]

# service = VocabularyService()
# vocabulary_id = service.create_vocabulary(prefix='prefix',
#                                         target_model='paraformer-realtime-v2',
#                                         vocabulary=my_vocabulary)

# print(f"your vocabulary id is {vocabulary_id}")


callback = Callback()
recognition = Recognition(model='paraformer-realtime-v2',
                          format='mp3',
                          sample_rate=16000,
                          callback=callback)
recognition.start()


with open("input1.mp3", "rb") as file:
    while chunk := file.read(1024):
        recognition.send_audio_frame(chunk)

#recognition.stop()

#time.sleep(5)  # 暂停 5 秒
#recognition.start()
with open("output1.mp3", "rb") as file:
    while chunk := file.read(1024):
        recognition.send_audio_frame(chunk)


recognition.stop()



#result = recognition.call('asr_example.wav')