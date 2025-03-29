# routes.py
# 路由模块，处理所有API路由

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from auth import require_auth

from models import get_model_list, map_model_name
from api_client import call_api
from response_formatter import format_openai_response

# 创建路由器
router = APIRouter()


@router.get("/v1/models")
async def list_models():
    """获取可用模型列表，兼容OpenAI格式"""
    return JSONResponse(content=get_model_list())


@router.post("/v1/chat/completions")
@require_auth
async def chat_completions(request: Request):
    """处理聊天完成请求，兼容OpenAI格式"""
    try:
        # 获取请求体
        body = await request.json()
        
        # 获取并映射模型名称
        model_name = body.get("model")
        mapped_model = map_model_name(model_name)
        
        # 构造转发请求体
        payload = {
            "messages": body.get("messages", []),
            "model": mapped_model
        }
        
        # 检查是否是流式请求
        is_stream = body.get("stream", False)
        
        # 调用API
        if is_stream:
            # 流式响应直接返回
            return await call_api(payload, is_stream=True)
        else:
            # 非流式响应需要格式化
            content = await call_api(payload, is_stream=False)
            return format_openai_response(content, model=mapped_model)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))