# models.py
# 模型映射和管理模块

# 可用模型列表，兼容OpenAI格式
AVAILABLE_MODELS = [
    {
        "id": "deepseek-r1-70b",
        "object": "model",
        "created": 1677610602,
        "owned_by": "deepseek",
        "permission": [],
        "root": "deepseek70b",
        "parent": None
    },
    {
        "id": "deepseek-r1-turbo",
        "object": "model",
        "created": 1677650000,
        "owned_by": "deepseek",
        "permission": [],
        "root": "deepseekr1turbo",
        "parent": None
    },
    {
        "id": "deepseek-v3-turbo",
        "object": "model",
        "created": 1677650100,
        "owned_by": "deepseek",
        "permission": [],
        "root": "deepseekv3turbo",
        "parent": None
    },
    {
        "id": "deepseek-v3-0324",
        "object": "model",
        "created": 1677650200,
        "owned_by": "deepseek",
        "permission": [],
        "root": "deepseekv30324",
        "parent": None
    },
    {
        "id": "deepseek-r1-search",
        "object": "model",
        "created": 1677650300,
        "owned_by": "deepseek",
        "permission": [],
        "root": "volcengine",
        "parent": None
    },
    {
        "id": "grok-3",
        "object": "model",
        "created": 1677650400,
        "owned_by": "xai",
        "permission": [],
        "root": "grok3",
        "parent": None
    },
    {
        "id": "grok-3-search",
        "object": "model",
        "created": 1677650500,
        "owned_by": "xai",
        "permission": [],
        "root": "grok3search",
        "parent": None
    },
    {
        "id": "grok-3-deepsearch",
        "object": "model",
        "created": 1677650600,
        "owned_by": "xai",
        "permission": [],
        "root": "grok3deepsearch",
        "parent": None
    },
    {
        "id": "grok-3-reasoning",
        "object": "model",
        "created": 1677650700,
        "owned_by": "xai",
        "permission": [],
        "root": "grok3reasoning",
        "parent": None
    },
    {
        "id": "qwen-32b",
        "object": "model",
        "created": 1677650800,
        "owned_by": "alibaba",
        "permission": [],
        "root": "qwen32b",
        "parent": None
    }
]

# 模型映射
MODEL_MAPPING = {
    "deepseek-r1-70b": "deepseek70b",
    "deepseek-r1-turbo": "deepseekr1turbo",
    "deepseek-ai/DeepSeek-R1-Turbo": "deepseekr1turbo",
    "deepseek-ai/DeepSeek-V3-Turbo": "deepseekv3turbo",
    "deepseek-v3-turbo": "deepseekv3turbo",
    "deepseek-v3-0324": "deepseekv30324",
    "deepseek-r1-search": "volcengine",
    "grok-3": "grok3",
    "grok-3-search": "grok3search",
    "grok-3-deepsearch": "grok3deepsearch",
    "grok-3-reasoning": "grok3reasoning",
    "qwen-32b": "qwen32b",
    "qwq-32b": "qwen32b"
}

# 默认模型
DEFAULT_MODEL = "deepseek70b"


def get_model_list():
    """获取所有可用模型列表，兼容OpenAI格式"""
    return {
        "object": "list",
        "data": AVAILABLE_MODELS
    }


def map_model_name(model_name):
    """将请求中的模型名称映射到内部使用的模型名称
    
    Args:
        model_name: 请求中指定的模型名称
        
    Returns:
        映射后的内部模型名称
    """
    if not model_name:
        return DEFAULT_MODEL
        
    return MODEL_MAPPING.get(model_name, DEFAULT_MODEL)