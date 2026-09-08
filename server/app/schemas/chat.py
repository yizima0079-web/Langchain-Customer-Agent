"""AI 客服对话相关请求/响应模型。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    """客服对话请求。"""

    session_id: str | None = Field(None, description="会话ID，首次可为空")
    message: str = Field(..., min_length=1, description="用户问题")


class ChatResponse(BaseModel):
    """客服对话响应。"""

    session_id: str
    answer: str
    # 命中的知识库来源片段（便于排查/展示）
    sources: list[str] = []


class ChatMessageOut(BaseModel):
    """单条聊天记录响应。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: str
    role: str
    content: str
    created_at: datetime | None = None
