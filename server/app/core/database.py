"""数据库引擎与会话管理（SQLAlchemy 2.0）。"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# 创建数据库引擎（MySQL 8，端口 3306）
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,      # 每次取连接前探测有效性，避免连接失效
    pool_recycle=3600,       # 连接回收周期（秒）
    echo=settings.DEBUG,     # 调试模式下打印 SQL
)

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 模型基类，所有模型继承自它
Base = declarative_base()
