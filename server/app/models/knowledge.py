"""知识库文件与聊天记录 ORM 模型。"""
from sqlalchemy import BigInteger, Column, DateTime, Integer, SmallInteger, String, Text, func

from app.core.database import Base


class KnowledgeFile(Base):
    """知识库文件表模型，记录上传文档及其向量化状态。"""

    __tablename__ = "knowledge_file"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="文件ID")
    filename = Column(String(255), nullable=False, comment="原始文件名")
    file_type = Column(String(16), nullable=False, comment="文件类型:txt/doc/pdf/markdown")
    file_path = Column(String(500), nullable=False, comment="本地存储路径")
    size = Column(Integer, nullable=False, default=0, comment="文件大小(字节)")
    status = Column(
        SmallInteger, nullable=False, default=0, comment="0=待处理 1=已向量化 2=处理失败"
    )
    chunk_count = Column(Integer, nullable=False, default=0, comment="切分文本块数量")
    error_msg = Column(String(500), nullable=True, comment="失败原因")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="上传时间")


class ChatMessage(Base):
    """聊天记录表模型，记录 AI 客服对话历史。"""

    __tablename__ = "chat_message"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="消息ID")
    user_id = Column(BigInteger, nullable=True, comment="用户ID(游客为NULL)")
    session_id = Column(String(64), nullable=False, comment="会话ID")
    role = Column(String(16), nullable=False, comment="角色:user/assistant")
    content = Column(Text, nullable=False, comment="消息内容")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="发送时间")
