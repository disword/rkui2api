# response_formatter.py
# 响应格式化模块，处理OpenAI格式的响应

import time
import uuid


def format_openai_response(content, model="deepseek70b"):
    """将内容格式化为OpenAI兼容的响应格式
    
    Args:
        content: 响应内容
        model: 使用的模型名称
        
    Returns:
        OpenAI格式的响应对象
    """
    # 生成唯一的响应ID
    response_id = f"chatcmpl-{uuid.uuid4().hex[:10]}"
    
    # 获取当前时间戳
    created_timestamp = int(time.time())
    
    return {
        "id": response_id,
        "object": "chat.completion",
        "created": created_timestamp,
        "model": model,  # 添加模型信息
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": content
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }


def format_openai_stream_chunk(content, model="deepseek70b", is_first_chunk=False, is_last_chunk=False):
    """格式化流式响应的单个数据块为OpenAI兼容格式
    
    Args:
        content: 当前数据块的内容
        model: 使用的模型名称
        is_first_chunk: 是否为第一个数据块
        is_last_chunk: 是否为最后一个数据块
        
    Returns:
        OpenAI格式的流式响应数据块
    """
    # 生成唯一的响应ID（对于同一流式响应，ID应保持一致）
    # 在实际应用中，应该在外部生成并传入
    response_id = f"chatcmpl-{uuid.uuid4().hex[:10]}"
    
    # 获取当前时间戳
    created_timestamp = int(time.time())
    
    response = {
        "id": response_id,
        "object": "chat.completion.chunk",
        "created": created_timestamp,
        "model": model,
        "choices": [{
            "index": 0,
            "delta": {},
            "finish_reason": None
        }]
    }
    
    # 第一个数据块需要包含角色信息
    if is_first_chunk:
        response["choices"][0]["delta"] = {
            "role": "assistant",
            "content": content
        }
    # 最后一个数据块需要包含完成原因
    elif is_last_chunk:
        response["choices"][0]["delta"] = {"content": content}
        response["choices"][0]["finish_reason"] = "stop"
    # 中间数据块只包含内容
    else:
        response["choices"][0]["delta"] = {"content": content}
    
    return response