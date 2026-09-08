"""速率限制器（slowapi），防止登录/注册等敏感接口被暴力破解。"""
from slowapi import Limiter
from slowapi.util import get_remote_address

# 按客户端 IP 限流，供路由用 @limiter.limit 装饰器引用
limiter = Limiter(key_func=get_remote_address)
