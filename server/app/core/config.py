"""应用全局配置模块。

从环境变量 / .env 文件读取配置，集中管理数据库、认证、LLM、向量库等参数。
"""
import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类，字段名与环境变量名一一对应（大小写不敏感）。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---- 应用基础 ----
    PROJECT_NAME: str = "基于LangChain的带AI智能客服的微信小程序商城系统"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # ---- 数据库（MySQL 8，端口 3306）----
    # host 使用 localhost：某些环境下服务器仅监听 IPv6(::1)，
    # 127.0.0.1(IPv4) 无法连接，而 localhost 由系统自动回退解析
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "MySQL@123456"
    MYSQL_DB: str = "shop_agent"

    # ---- 认证 ----
    JWT_SECRET: str = "change-me-to-a-random-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # ---- 文件上传 ----
    UPLOAD_DIR: str = "F:/uploads14"

    # ---- LLM（OpenAI 兼容接口，DashScope）----
    OPENAI_API_BASE: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    LLM_MODEL: str = "qwen3.8-flash"
    EMBEDDING_MODEL: str = "qwen3.7-text-embedding-flash"
    # 嵌入向量维度：qwen3.7-text-embedding-flash 实测最大支持 1024
    EMBEDDING_DIM: int = 1024
    LLM_TEMPERATURE: float = 0.7
    # 大模型访问密钥（用户指定名称 OPENAL_APLKEY；OS 环境变量优先级高于 .env）
    OPENAL_APLKEY: str = ""

    # ---- Chroma 向量库 ----
    CHROMA_DIR: str = "F:/uploads14/chroma"

    # ---- CORS ----
    # 逗号分隔的字符串（env 便于书写，使用 cors_origin_list 取值）
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        """将逗号分隔的 CORS 配置解析为列表。"""
        return [x.strip() for x in self.CORS_ORIGINS.split(",") if x.strip()]

    @property
    def database_url(self) -> str:
        """拼接 SQLAlchemy 数据库连接串。

        密码可能含特殊字符，需做 URL 编码，避免连接串解析异常。
        """
        from urllib.parse import quote_plus

        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{quote_plus(self.MYSQL_PASSWORD)}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}?charset=utf8mb4"
        )

    @property
    def api_key(self) -> str:
        """读取大模型访问密钥。

        pydantic-settings 已自动合并 .env 与 OS 环境变量的 OPENAL_APLKEY
        （OS 环境变量优先）；再兼容回退 OpenAI 标准变量名 OPENAI_API_KEY。
        """
        return (self.OPENAL_APLKEY or "").strip() or os.getenv("OPENAI_API_KEY") or ""


@lru_cache
def get_settings() -> Settings:
    """返回缓存的全局配置单例。"""
    return Settings()


settings = get_settings()
