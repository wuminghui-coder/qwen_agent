import json
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import logging
from extensions.exten_sql import SessionDep

logger = logging.getLogger(__name__)

# 抽象基类
class BuiltinTool(ABC):
    @abstractmethod
    def _invoke(self, 
                user:str,
                conversation_id:str, 
                tool_parameters: dict[str, Any])->Optional[Any]:
        pass
