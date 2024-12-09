import json
from typing import Dict, List, Optional
from openai import OpenAI

class OpenAILLM():
    def __init__(self, 
                 model:str, 
                 api_key:str,
                 base_url:str,
                 temperature: float = 0, 
                 top_p: float = 0, 
                 max_tokens: int = 3000):
        
        self.model       = model
        self.temperature = temperature
        self.max_tokens  = max_tokens
        self.top_p       = top_p

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
    def _parse_response(self, response, tools):
        if tools:
            processed_response = {
                "content": response.choices[0].message.content,
                "tool_calls": [],
            }

            if response.choices[0].message.tool_calls:
                for tool_call in response.choices[0].message.tool_calls:
                    processed_response["tool_calls"].append(
                        {
                            "name": tool_call.function.name,
                            "arguments": json.loads(tool_call.function.arguments),
                        }
                    )

            return processed_response
        else:
            return response.choices[0].message.content

    def generate_response(
        self,
        messages: List[Dict[str, str]],
        response_format=None,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
    ):
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p
        }

        if response_format:
            params["response_format"] = response_format
        if tools:  # TODO: Remove tools if no issues found with new memory addition logic
            params["tools"] = tools
            params["tool_choice"] = tool_choice

        response = self.client.chat.completions.create(**params)
        return self._parse_response(response, tools)
