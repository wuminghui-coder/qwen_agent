from core.tools_call.tools import BuiltinTool
from typing import Dict, List, Optional, Any
from extensions.exten_sql import SessionDep
from core.music_agent import MusicAgent
# Dog 类实现
class Dog(BuiltinTool):
    
    def _invoke(self, 
                user:str, 
                conversation_id:str, 
                tool_parameters: dict[str, Any])->Optional[Any]:
        
        music_agent = tool_parameters.get("wmusic")
        if not music_agent:
            return None

        return music_agent.get_song_by_name(tool_parameters.get("song's name"))