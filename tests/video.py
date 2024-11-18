import requests
import json

def synthesize_video(api_key, image_url, audio_url, face_bbox, ext_bbox):
    url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis/'
    
    headers = {
        'X-DashScope-Async': 'enable',
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "model": "emo-v1",
        "input": {
            "image_url": image_url,
            "audio_url": audio_url,
            "face_bbox": face_bbox,
            "ext_bbox": ext_bbox
        },
        "parameters": {
            "style_level": "normal"
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()  # 返回成功响应的 JSON 数据
    else:
        return {
            "error": response.status_code,
            "message": response.text
        }

# 示例用法
api_key = 'sk-d4a24c9626034f5384a68490f983f97b'  # 替换为你的实际 API 密钥
image_url = 'https://base-pri.oss-cn-shenzhen.aliyuncs.com/ac008546bc7f7ed1de652d7678cb552.jpg?x-oss-credential=LTAI5tP92MbM8XQksAPd5VbJ%2F20241114%2Fcn-shenzhen%2Foss%2Faliyun_v4_request&x-oss-date=20241114T090227Z&x-oss-expires=3600&x-oss-signature-version=OSS4-HMAC-SHA256&x-oss-signature=74faa953a0bbe2148db3f42b5922c6e11c4656be3fb13b8a3807e0f6323523fe'
audio_url = 'https://base-pri.oss-cn-shenzhen.aliyuncs.com/b7c15681f5531aa35d75b7175523b9ae.mp3?x-oss-credential=LTAI5tP92MbM8XQksAPd5VbJ%2F20241114%2Fcn-shenzhen%2Foss%2Faliyun_v4_request&x-oss-date=20241114T084516Z&x-oss-expires=3600&x-oss-signature-version=OSS4-HMAC-SHA256&x-oss-signature=98a033a7e1bcd504a187d50c693480346855746189a1c63f9d5ac69e65e765f4'
face_bbox = [387, 188, 769, 570]
ext_bbox = [225, 0, 931, 706]

# result = synthesize_video(api_key, image_url, audio_url, face_bbox, ext_bbox)
# print(result)


def a_synthesize_video(api_key, image_url):
    url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/face-detect'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "model": "emo-detect-v1",
        "input": {
            "image_url": image_url,
          
        },
        "parameters": {
            "ratio": "1:1"
        }
    }

    response = requests.post(url=url, headers=headers, data=json.dumps(data))
    return response.json()
# resp = a_synthesize_video(api_key, image_url)

# print(resp)

def get_synthesize_video(api_key):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url="https://dashscope.aliyuncs.com/api/v1/tasks/facc584e-5097-432a-916d-a6afdf8c46e9", headers=headers)
    return response.json()

resp = get_synthesize_video(api_key)
print(resp)