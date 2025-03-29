# auth.py
# 身份验证中间件，处理API请求的认证

from fastapi import Request, HTTPException
from functools import wraps
from config import AuthConfig

def verify_token(request: Request) -> bool:
    """验证请求中的Bearer Token
    
    Args:
        request: FastAPI请求对象
        
    Returns:
        bool: 令牌是否有效
    """
    auth_header = request.headers.get('Authorization')
    return AuthConfig.validate_token(auth_header)

def require_auth(func):
    """要求认证的装饰器
    
    用法:
        @require_auth
        async def protected_route():
            ...
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get('request')
        if not request:
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
        
        if not request:
            raise HTTPException(status_code=500, detail="Internal server error")
            
        if not verify_token(request):
            raise HTTPException(
                status_code=401,
                detail="Invalid or missing authentication token",
                headers={"WWW-Authenticate": "Bearer"}
            )
            
        return await func(*args, **kwargs)
    
    return wrapper