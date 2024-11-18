import requests
import json

header = {
    "Content-Type": "application/json"
}

body= {
    "url":"https://news.cctv.com/world/"
}

response = requests.post(url="http://localhost:3002/v0/scrape", data=json.dumps(body), headers=header )

resp = json.loads(response.text)

json_string = json.dumps(resp, indent=4, separators=(',', ': '), ensure_ascii=False)
print(json_string)
print(resp["data"]["content"])
