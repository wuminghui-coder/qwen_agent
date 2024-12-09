from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Mem0Settings(BaseSettings):
    LLM_MODEL: str = Field(default="gpt-4o", description="model")
    LLM_TEMPERATURE:float = Field(default=0.2, description="model")
    LLM_MAX_TOKENS:int = Field(default=2000, description="model")
    LLM_URL: str = Field(default="https://dashscope.aliyuncs.com/compatible-mode/v1", description="model")
    LLM_KEY: str = Field(default="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", description="model")

    QDRANT_NAME: str = Field(default="qdrant", description="model")
    QDRANT_HOST : str = Field(default="localhost", description="model")
    QDRANT_PORT:int = Field(default=6333, description="model")


    EMBEDDING_MODEL: str = Field(default="bge-base-zh-v1.5", description="model")
    EMBEDDING_URL: str = Field(default="http://172.16.100.200:9997/v1", description="model")
    EMBEDDING_DIMS:int = Field(default=768, description="model")
    
    RERANK_MODE: str = Field(default="bge-reranker-base", description="model")
    RERANK_URL: str = Field(default="http://172.16.100.200:9997/v1/rerank", description="model")

    ENABLE_RERANK:bool = Field(default=False, description="")
    SCORE:float = Field(default=0.5, description="model")
    RELEVANCE_SCORE:float= Field(default=0.5, description="model")

    @property
    def get_mem0_config(self)->dict:
        return {
                "llm": {
                    "provider": "openai",
                    "config": {
                        "api_key":self.LLM_KEY,
                        "model": self.LLM_MODEL,
                        "temperature": self.LLM_TEMPERATURE,
                        "max_tokens": self.LLM_MAX_TOKENS,
                        #"openai_base_url": self.LLM_URL
                    }
                },

                "vector_store": {
                    "provider": "qdrant",
                    "config": {
                        "collection_name": self.QDRANT_NAME,
                        "host": self.QDRANT_HOST,
                        "embedding_model_dims": self.EMBEDDING_DIMS,
                        "port": self.QDRANT_PORT,
                    }
                },

                "embedder": {
                    "provider": "openai",
                    "config": {
                        "api_key":self.LLM_KEY,
                        "model": self.EMBEDDING_MODEL,
                        "embedding_dims": self.EMBEDDING_DIMS,
                        "openai_base_url": self.EMBEDDING_URL
                    }
                },
                "version": "v1.1",
        }

