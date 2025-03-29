# config.py
# 配置模块，管理环境变量和配置项

import os
from typing import Optional

# API认证配置
class AuthConfig:
    # 从环境变量获取API令牌，如果未设置则使用默认值
    API_TOKEN: str = os.getenv('API_TOKEN', 'sk-114514')
    
    @classmethod
    def get_token(cls) -> str:
        """获取API认证令牌
        
        Returns:
            str: API认证令牌
        """
        return cls.API_TOKEN
    
    @classmethod
    def validate_token(cls, token: Optional[str]) -> bool:
        """验证API令牌是否有效
        
        Args:
            token: 待验证的令牌
            
        Returns:
            bool: 令牌是否有效
        """
        if not token:
            return False
        
        # 移除Bearer前缀并验证
        if token.startswith('Bearer '):
            token = token[7:]
        
        return token == cls.API_TOKEN