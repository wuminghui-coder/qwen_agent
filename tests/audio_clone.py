import os
import dashscope
from dashscope.audio.tts_v2 import VoiceEnrollmentService, SpeechSynthesizer

dashscope.api_key = "sk-d4a24c9626034f5384a68490f983f97b"  # 如果您没有配置环境变量，请在此处用您的API-KEY进行替换
#url = "https://base-pri.oss-cn-shenzhen.aliyuncs.com/input.mp3?x-oss-credential=LTAI5tP92MbM8XQksAPd5VbJ%2F20241114%2Fcn-shenzhen%2Foss%2Faliyun_v4_request&x-oss-date=20241114T071345Z&x-oss-expires=3600&x-oss-signature-version=OSS4-HMAC-SHA256&x-oss-signature=f0565f11b593b278abec6dfd58b9ddb46b90bbfed2fb99144db8157618add3eb"  # 请按实际情况进行替换

#url = "https://base-pri.oss-cn-shenzhen.aliyuncs.com/1d39fb8367c1f1b55da29cb7f9fcfcd8.mp3?x-oss-credential=LTAI5tP92MbM8XQksAPd5VbJ%2F20241114%2Fcn-shenzhen%2Foss%2Faliyun_v4_request&x-oss-date=20241114T072544Z&x-oss-expires=3600&x-oss-signature-version=OSS4-HMAC-SHA256&x-oss-signature=2238ab782282311c5dd945d1a83749b4dd195c95ac6d65658327147fa1b7d69d"
url = "https://base-pri.oss-cn-shenzhen.aliyuncs.com/b7c15681f5531aa35d75b7175523b9ae.mp3?x-oss-credential=LTAI5tP92MbM8XQksAPd5VbJ%2F20241114%2Fcn-shenzhen%2Foss%2Faliyun_v4_request&x-oss-date=20241114T072608Z&x-oss-expires=3600&x-oss-signature-version=OSS4-HMAC-SHA256&x-oss-signature=b4b94690f703be99e0477e91899080e4f32735103d6da9e0ee03741e7186a004"

#url="https://base-pri.oss-cn-shenzhen.aliyuncs.com/f16b8c208a1275e7395e56e26c733ab2.mp3?x-oss-credential=LTAI5tP92MbM8XQksAPd5VbJ%2F20241114%2Fcn-shenzhen%2Foss%2Faliyun_v4_request&x-oss-date=20241114T072629Z&x-oss-expires=3600&x-oss-signature-version=OSS4-HMAC-SHA256&x-oss-signature=eb834b02959cf849a669c2a5686e8f570f3986ba0879efa979f29485734ee702"

prefix = 'prefix'
target_model = "cosyvoice-clone-v1"

# 创建语音注册服务实例
service = VoiceEnrollmentService()

# 调用create_voice方法复刻声音，并生成voice_id
# voice_id = service.create_voice(target_model=target_model, prefix=prefix, url=url)
# print(f"your voice id is {voice_id}")

# 使用复刻的声音进行语音合成
synthesizer = SpeechSynthesizer(model=target_model, voice="cosyvoice-prefix-10ddd328929f4d4da543f6add341c8b0")
audio = synthesizer.call("绵心是未来华东师范大学的学生")
print("requestId: ", synthesizer.get_last_request_id())

# 将合成的音频文件保存到本地文件
with open("output.mp3", "wb") as f:
    f.write(audio)

#sh converter.sh test.slk mp3



print(service.list_voices(prefix=None, page_index= 0, page_size=10))