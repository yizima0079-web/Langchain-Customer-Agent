"""Chroma 向量数据库封装（持久化 + 单例）。"""
from langchain_community.vectorstores import Chroma

from app.core.config import settings
from app.services.embeddings import get_embeddings

# 向量集合名称，知识库统一写入该集合
COLLECTION_NAME = "knowledge_base"

# 模块级缓存
_vectorstore: Chroma | None = None


def get_vectorstore() -> Chroma:
    """获取 Chroma 向量库单例。

    持久化目录由配置 CHROMA_DIR 指定，嵌入函数复用全局单例。

    Returns:
        Chroma 向量库实例。
    """
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=get_embeddings(),
            persist_directory=settings.CHROMA_DIR,
        )
    return _vectorstore


def add_documents(documents: list) -> int:
    """将文档块写入向量库。

    Args:
        documents: 已切分的 Document 列表。

    Returns:
        写入的文档块数量。
    """
    if not documents:
        return 0
    get_vectorstore().add_documents(documents)
    return len(documents)
