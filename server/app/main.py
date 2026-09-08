"""FastAPI 应用入口。

负责创建应用实例、注册中间件、挂载静态目录与各业务路由。
"""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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
