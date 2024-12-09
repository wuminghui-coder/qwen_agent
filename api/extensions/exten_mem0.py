from core.api_service.mem0_api import Mem0Api
from  config.app_config import settings

mem0_api = Mem0Api(config=settings.get_mem0_config, 
            enable_rerank=settings.ENABLE_RERANK,
            rerank_url=settings.RERANK_URL, 
            rerank_mode=settings.RERANK_MODE,
            score = settings.SCORE,
            relevance_score= settings.RELEVANCE_SCORE)