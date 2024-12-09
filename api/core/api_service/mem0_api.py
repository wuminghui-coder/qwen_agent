from mem0 import Memory
from typing import Optional
import requests
import json
import logging
from tasks.add_memory_task import add_memory_task
logger = logging.getLogger(__name__)

class Mem0Api():
    def __init__(self, config: dict, 
                 enable_rerank:bool=False,
                 rerank_mode:Optional[str] = None, 
                 rerank_url:Optional[str] = None, 
                 score: float = 0.5,
                 relevance_score: float = 0.5):
        self.memory = Memory.from_config(config)
        self.enable_rerank = enable_rerank
        self.rerank_mode = rerank_mode
        self.rerank_url  = rerank_url
        self.score = score
        self.relevance_score = relevance_score

    def add_memories(self, memory: str, user_id: str):
        self.memory.add(messages=memory, user_id=user_id)

    def _get_memories(self, user_id)->Optional[list]:
        memories = self.memory.get_all(user_id=user_id)
        if not memories.get('results'):
            return None
        return [m['memory'] for m in memories['results']]

    def _search_memories(self, query, user_id)->Optional[list]:
        memories = self.memory.search(query, user_id=user_id)
        if not memories.get('results'):
            return None
        return [m['memory'] for m in memories['results'] if m['score'] > self.score]
    
    def get_memories(self, question:str, user_id: str)->Optional[str]:
        previous_memories = self._search_memories(question, user_id=user_id)
        if not previous_memories:
            add_memory_task.delay(question, user_id)
            return question
        
        if self.enable_rerank:
            previous_memories = self._rerank_query(question, previous_memories)

        add_memory_task.delay(question, user_id)

        return f"User input: {question}\n Previous memories: {previous_memories}"

    def _rerank_query(self, query:str, corpus:list)->Optional[list]:
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        body = {
            "model": self.rerank_mode,
            "query": query,
            "documents": corpus,
            'return_documents': True
        }

        resp = requests.post(url=self.rerank_url, headers=headers, data=json.dumps(body))
        if resp.status_code!= 200:
            logger.error(f"Failed to rerank documents, status code: {resp.status_code}")
            return None
        
        try:
            resp_json = json.loads(resp.text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        
        rerank_resp = []
        for item in resp_json["results"]:
            if item["relevance_score"] > self.relevance_score:
                rerank_resp.append(item["document"])

        return rerank_resp if rerank_resp else None
