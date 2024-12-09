import json
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
from core.tools_call.tools_util import load_yaml_files, load_tools_classes
import logging
from extensions.exten_sql import SessionDep

logger = logging.getLogger(__name__)

class ToolsService():
    def __init__(self):
        self.tool_list = load_yaml_files('core/tools_call/provide')

    def invoke_tools(self, user:str,
                        conversation_id:str, 
                        tool_name: str, 
                        tool_parameters: Optional[dict[str, Any]] = None)->Optional[Any]:
        
        for item_tool in self.tool_list:
            if item_tool["name"] == tool_name:
                tool_class = load_tools_classes(item_tool["module_name"])
                if not tool_name:
                    logger.error(f"找不到工具:{tool_name}")
                    return None
                animal_instance = tool_class()       # 创建实例
                return animal_instance._invoke(user=user, 
                                               conversation_id=conversation_id,
                                               tool_parameters=tool_parameters)     # 调用 speak 方法

    def get_tools_config(self, tool_name: str)->Optional[dict]:
        for item_tool in self.tool_list:
            if item_tool["name"] == tool_name:
                return item_tool["config"]
        return None
    @property
    def get_all_tools_name(self)->Optional[list]:
        tools_name = []
        for item_tool in self.tool_list:
            tools_name.append(item_tool["name"])
        return tools_name
         

tools_service = ToolsService()