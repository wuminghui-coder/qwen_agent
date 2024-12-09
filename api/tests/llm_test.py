import sys
import os
import yaml
from typing import Optional
# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 添加上级目录到 sys.path
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

sys.path.append(parent_dir)

from core.api_service.llm import OpenAILLM
from config.app_config import settings
from core.prompt import MUSIC_PROMPT, CHAT_PROMPT,MUSIC_PROMPT_TEST,ARTIST_PROMPT_TEST, WEATHER_PROMPT
from core.prompt import MUSIC_PROMPT, CHAT_PROMPT
from core.api_service.llm import OpenAILLM
from core import function_call

import time

tools=[{"type" : "function",
        "function": {
            "name":"get_current_weather",
            "description":"get the current weather in a given location",
            "parameters":{ 
                "type":"object",
                "properties": {
                    "city": {
                        "type":"string",
                         "description":"the city and state, e,g.San Franciso, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required":["city"],
            },
        }
    }
]

qwen_agent = OpenAILLM(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_KEY,
        base_url=settings.OPENAI_URL,
        temperature=0.8,
        top_p=0.9,
        max_tokens=settings.OPENAI_MAX_TOKEN,
)


messages = [{"role": "system", "content": CHAT_PROMPT}]

def main():
    while True:
        question = input("Question: ")
        if question.lower() in ['q', 'exit']:
            print("Exiting...")
            break

        current_timestamp = int(time.time() * 1000)

        messages.append({"role": "user", "content": question})

        answer = qwen_agent.generate_response(messages, tools=[function_call.weather_config])

        print(answer)
        content = answer["content"]
        messages.append({"role": "assistant", "content": content})

        current_timestamp1 = int(time.time() * 1000) - current_timestamp
        print(f"Answer {current_timestamp1}ms: {content}")
    
    for msg in messages:
        print(f"{msg['role']}: {msg['content']}")

if __name__ == "__main__":
    main()