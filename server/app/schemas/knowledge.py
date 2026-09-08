"""知识库相关响应模型。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class KnowledgeFileOut(BaseModel):
    """知识库文件响应。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    file_type: str
    file_path: str
    size: int
    status: int
    chunk_count: int
    error_msg: str | None = None
    created_at: datetime | None = None
