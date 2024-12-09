import importlib
import os
from core.tools_call.tools import BuiltinTool
import yaml
from  typing import Optional, Type
import logging

logger = logging.getLogger(__name__)

def create_openai_config(config: dict)->Optional[dict]:
    if not config.get("name") or not config.get("description"):
        logger.error("OpenAI 配置参数不完整。")
        return None
    
    tool_config = {
        "type" : "function", 
        "function": {
            "name":        config["name"],
            "description": config["description"],
            "parameters": {
                "type":"object", 
                "properties":{}, 
                "required":[]
            }
        },
    }

    if not config["parameters"]:
        return tool_config
    
    for item in config["parameters"]:
        tool_config["function"]["parameters"]["properties"][item["name"]] = {"type": item["type"], "description": item["description"]}
        if item["required"]:
            tool_config["function"]["parameters"]["required"].append(item["name"])

    return tool_config
    

def load_tools_classes(model_path: str)->Optional[Type[BuiltinTool]]:
    try:
        module = importlib.import_module(model_path)
    except ModuleNotFoundError:
        logger.error(f"模块 '{model_path}' 未找到。")
        return None
    except ImportError as e:
        logger.error(f"导入模块时发生错误: {e}")
        return None
    except Exception as e:
        logger.error(f"发生了其他错误: {e}")
        return None

    # 查找模块中的所有类
    for name in dir(module):
        cls = getattr(module, name)
        # 检查类是否是 Animal 的子类
        if isinstance(cls, type) and issubclass(cls, BuiltinTool) and cls is not BuiltinTool:
            return cls
    logger.error("导入的工具没有继承BuiltinTool类")
    return None

def load_yaml_files(directory)->Optional[list]:
    yaml_data = []
    # 使用 os.walk 遍历目录及其子目录
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    config = yaml.safe_load(file)  # 加载 YAML 文件
                    yaml_data.append({"file_path":root, 
                                      "name": config.get("name"),
                                      "config": create_openai_config(config),
                                      "module_name": root.replace("/", ".") + "." + config.get("filename")})  # 存储文件路径和数据
    return yaml_data
