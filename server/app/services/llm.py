"""聊天大模型封装（OpenAI 兼容接口，懒加载单例）。"""
from langchain_openai import ChatOpenAI

from app.core.config import settings

# 模块级缓存，避免每次请求重复创建连接
_llm: ChatOpenAI | None = None


def get_llm() -> ChatOpenAI:
    """获取聊天模型单例。

    首次调用时按配置构造 ChatOpenAI，之后复用同一实例。

    Returns:
        已配置的 ChatOpenAI 实例。
    """
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            base_url=settings.OPENAI_API_BASE,
            api_key=settings.api_key,
            temperature=settings.LLM_TEMPERATURE,
        )
    return _llm
