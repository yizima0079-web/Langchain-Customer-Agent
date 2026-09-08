"""FastAPI 应用入口。

负责创建应用实例、注册中间件、挂载静态目录与各业务路由。
"""
import logging
import os
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded

from app.api.routes import (
    address,
    auth,
    banner,
    cart,
    category,
    chat,
    health,
    knowledge,
    order,
    product,
    stats,
    upload,
    user,
)
from app.core.config import settings
from app.core.limiter import limiter

# 基础日志配置（格式含时间 / 级别 / 模块名）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

logger = logging.getLogger("app.main")


def create_app() -> FastAPI:
    """创建并配置 FastAPI 应用。

    Returns:
        FastAPI 应用实例。
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # 跨域中间件
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 全局异常处理：未捕获异常统一返回，避免堆栈泄露
    @application.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("未处理异常: %s %s (%s)", request.method, request.url.path, type(exc).__name__)
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": "服务器内部错误",
                "data": None,
                "detail": "服务器内部错误",
            },
        )

    # 请求日志中间件：记录方法 / 路径 / 状态码 / 耗时
    @application.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        logger.info(
            "%s %s -> %d (%.0fms)",
            request.method,
            request.url.path,
            response.status_code,
            (time.perf_counter() - start) * 1000,
        )
        return response

    # 速率限制：注册 limiter 到 app.state，超限返回 429
    application.state.limiter = limiter

    @application.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={
                "code": 429,
                "message": "请求过于频繁，请稍后再试",
                "data": None,
                "detail": "请求过于频繁",
            },
        )

    # 挂载上传目录为静态资源（供图片/文件访问）
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    application.mount(
        "/uploads14", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads14"
    )

    prefix = settings.API_PREFIX
    # 注册全部业务路由
    application.include_router(health.router, prefix=prefix)
    application.include_router(auth.router, prefix=prefix)
    application.include_router(banner.router, prefix=prefix)
    application.include_router(user.router, prefix=prefix)
    application.include_router(category.router, prefix=prefix)
    application.include_router(product.router, prefix=prefix)
    application.include_router(cart.router, prefix=prefix)
    application.include_router(order.router, prefix=prefix)
    application.include_router(address.router, prefix=prefix)
    application.include_router(upload.router, prefix=prefix)
    application.include_router(knowledge.router, prefix=prefix)
    application.include_router(chat.router, prefix=prefix)
    application.include_router(stats.router, prefix=prefix)

    return application


app = create_app()
