import dashscope
from dashscope.audio.tts_v2 import *
# format=
# WAV_8000HZ_MONO_16BIT

# WAV_16000HZ_MONO_16BIT

# WAV_22050HZ_MONO_16BIT

# WAV_24000HZ_MONO_16BIT

# WAV_44100HZ_MONO_16BIT

# WAV_48000HZ_MONO_16BIT

# MP3_8000HZ_MONO_128KBPS

# MP3_16000HZ_MONO_128KBPS

# MP3_22050HZ_MONO_256KBPS

# MP3_24000HZ_MONO_256KBPS

# MP3_44100HZ_MONO_256KBPS

# MP3_48000HZ_MONO_256KBPS

# PCM_8000HZ_MONO_16BIT

# PCM_16000HZ_MONO_16BIT

# PCM_22050HZ_MONO_16BIT

# PCM_24000HZ_MONO_16BIT

# PCM_44100HZ_MONO_16BIT

# PCM_48000HZ_MONO_16BIT
# 将your-dashscope-api-key替换成您自己的API-KEY
# dashscope.api_key = "sk-d4a24c9626034f5384a68490f983f97b"
# model = "cosyvoice-v1"
# voice = "longxiaochun"


# synthesizer = SpeechSynthesizer(model=model, voice=voice)
# audio = synthesizer.call("日前，教育部印发《关于做好2025届全国普通高校毕业生就业创业工作的通知》，部署各地各高校实施“2025届全国普通高校毕业生就业创业促进和服务体系建设行动”，全力促进高校毕业生高质量充分就业")
# print('requestId: ', synthesizer.get_last_request_id())
# with open('output.mp3', 'wb') as f:
#     f.write(audio)




# longwan
# longcheng
# longhua
# longxiaoxia
# longxiaocheng
# longxiaobai
# longlaotie
# longshu
# longshuo
# longjing
# longmiao
# longyue
# longyuan
# longfei
# longjielidou
# longtong
# longxiang
# loongstella
# loongbella


import dashscope
from dashscope.audio.tts_v2 import *

# 将your-dashscope-api-key替换成您自己的API-KEY
dashscope.api_key = "sk-d4a24c9626034f5384a68490f983f97b"
model = "cosyvoice-v1"
voice = "longxiaochun"


class Callback(ResultCallback):
    _player = None
    _stream = None

    def on_open(self):
        self.file = open("output.mp3", "wb")
        print("websocket is open.")

    def on_complete(self):
        print("speech synthesis task complete successfully.")

    def on_error(self, message: str):
        print(f"speech synthesis task failed, {message}")

    def on_close(self):
        print("websocket is closed.")
        self.file.close()

    def on_event(self, message):
        print(f"recv speech synthsis message {message}")

    def on_data(self, data: bytes) -> None:
        print("audio result length:", len(data))
        self.file.write(data)


callback = Callback()

synthesizer = SpeechSynthesizer(
    model=model,
    voice=voice,
    callback=callback,
)

synthesizer.call("今天天气怎么样？")
print('requestId: ', synthesizer.get_last_request_id())