from tools import BuiltinTool
from typing import Dict, List, Optional, Any
from extensions.exten_sql import SessionDep
# Dog 类实现
class Dog(BuiltinTool):
    
    def _invoke(self, 
                user:str, 
               
                conversation_id:str, 
                tool_parameters: dict[str, Any])->Optional[Any]:
        return "Woof!"