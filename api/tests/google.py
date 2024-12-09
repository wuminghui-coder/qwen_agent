import requests
import os
import json
# Step 1.构建请求
url = "https://www.googleapis.com/customsearch/v1"

# Step 2.设置查询参数（还有很多参数）
search_term = "Discipline means choices. Every time you say yes to a goal or objective, you say no to many more. Every prize has its price. The prize is the yes; the price the no. Igor Gorin, the"
params = {
    'q': search_term,           # 搜索关键词
    'key': "AIzaSyDp1mTacLy5GpqlV0XLBPsWj0IJV0xZhvQ",   # 谷歌搜索API Key
    'cx': "665e0aafb5cc940c6",
    "c2coff":0# CSE ID
}

# Step 3.发送GET请求
response = requests.get(url, params=params)

# Step 4.解析响应
resp = json.loads(response.text)

json_string = json.dumps(resp, indent=4, separators=(',', ': '), ensure_ascii=False)
print(json_string)
for item in resp["items"]:
    print(item["title"], item["link"], item["snippet"])
