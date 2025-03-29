# api_client.py
# API客户端模块，处理与目标API的通信

import httpx
import json
import asyncio
import random
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from random_user_agent.user_agent import UserAgent


def generate_random_user_agent():
    """生成随机的User-Agent字符串
    
    Returns:
        随机生成的User-Agent字符串
    """
    # 使用random-user-agent库生成随机User-Agent
    user_agent_rotator = UserAgent()
    return user_agent_rotator.get_random_user_agent()


async def call_api(payload, is_stream=False):
    """调用目标API并处理响应
    
    Args:
        payload: 请求负载
        is_stream: 是否为流式请求
        
    Returns:
        流式响应或完整内容
    """
    try:
        async with httpx.AsyncClient() as client:
            # 生成随机User-Agent
            user_agent = generate_random_user_agent()
            
            # 发送请求到目标API
            response = await client.post(
                "https://deepseek.rkui.cn/api/chat",
                json=payload,
                timeout=60.0,
                headers={
                    "Accept": "text/event-stream",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "User-Agent": user_agent
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            # 检查响应内容是否为空
            if not response.content:
                raise HTTPException(status_code=502, detail="Empty response from API")
                
            # 处理流式响应
            if is_stream:
                return handle_stream_response(response)
            
            # 处理非流式响应
            return await handle_non_stream_response(response)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def handle_stream_response(response):
    """处理流式响应
    
    Args:
        response: API响应对象
        
    Returns:
        StreamingResponse对象
    """
    async def generate():
        buffer = ""
        chunk_count = 0  # 用于跟踪接收到的数据块数量
        
        print("\n===== 开始接收API响应数据 =====\n")
        
        # 使用aiter_text处理文本流，确保实时处理
        async for chunk in response.aiter_text():
            chunk_count += 1
            print(f"\n[接收数据块 #{chunk_count}] 原始数据: {chunk!r}\n")
            
            # 立即处理接收到的数据块
            buffer += chunk
            
            # 处理缓冲区中的每一行
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                
                # 处理完整的SSE行
                if line.startswith("data: "):
                    print(f"\n[SSE行] {line}")
                    
                    if line == "data: [DONE]":
                        print("\n===== 接收到完成标记 [DONE] =====\n")
                        # 确保立即发送完成标记
                        yield "data: [DONE]\n\n"
                        # 强制刷新缓冲区
                        await asyncio.sleep(0)
                        continue
                    
                    try:
                        # 直接转发SSE行，不尝试解析JSON
                        # 确保行以data:开头并以\n\n结尾
                        formatted_response = f"{line}\n\n"
                        print(f"[直接转发SSE行] {formatted_response!r}")
                        # 立即发送数据，不等待整个响应完成
                        yield formatted_response
                        # 强制刷新缓冲区，确保数据立即发送
                        await asyncio.sleep(0)
                        # 添加额外的刷新，确保数据立即发送到客户端
                        await asyncio.sleep(0.01)
                    except Exception as e:
                        print(f"\n[处理行时出错] 错误类型: {type(e).__name__}, 错误信息: {e}\n[问题数据] {line!r}")
                        continue
        
        print("\n===== API响应数据接收完毕 =====\n")
        if buffer:
            print(f"[剩余未处理的缓冲区数据] {buffer!r}")
    
    # 使用headers参数明确设置Content-Type，确保不包含charset=utf-8
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )


async def handle_non_stream_response(response):
    """处理非流式响应
    
    Args:
        response: API响应对象
        
    Returns:
        提取的完整内容
    """
    full_content = ""
    buffer = ""
    print("\n===== 开始接收非流式API响应数据 =====\n")
    
    # 立即处理每个数据块，不等待整个响应完成
    async for chunk in response.aiter_text():
        print(f"\n[接收非流式数据块] 原始数据: {chunk!r}\n")
        
        # 立即处理接收到的数据块
        buffer += chunk
        
        # 处理缓冲区中的每一行
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            
            # 处理完整的SSE行
            if line.startswith("data: "):
                print(f"\n[非流式SSE行] {line}")
                
                if line == "data: [DONE]":
                    print("\n===== 接收到非流式完成标记 [DONE] =====\n")
                    # 强制刷新缓冲区
                    await asyncio.sleep(0)
                    continue
                
                try:
                    # 提取SSE行中的JSON数据
                    json_str = line[6:]  # 去掉 "data: " 前缀
                    data = json.loads(json_str)
                    if "choices" in data and len(data["choices"]) > 0:
                        delta = data["choices"][0].get("delta", {})
                        content = delta.get("content", "")
                        full_content += content
                        # 强制刷新缓冲区
                        await asyncio.sleep(0)
                except Exception as e:
                    print(f"\n[处理非流式行时出错] 错误类型: {type(e).__name__}, 错误信息: {e}\n[问题数据] {line!r}")
                    continue
    
    print("\n===== 非流式API响应数据接收完毕 =====\n")
    if buffer:
        print(f"[剩余未处理的缓冲区数据] {buffer!r}")        
    # 如果没有成功提取内容，尝试直接解析响应
    if not full_content:
        try:
            data = response.json()
            full_content = data.get("content", "")
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=502,
                detail=f"Invalid JSON response from API: {response.text[:200]}"
            )
            
    return full_content
