"""文本嵌入封装（DashScope OpenAI 兼容接口）。

langchain-openai 1.6 的 OpenAIEmbeddings 封装存在传参 bug（请求 input 被包成
对象导致网关 400），因此直接基于 openai client 实现 LangChain Embeddings 接口，
行为可控、与裸调用一致。
"""
from langchain_core.embeddings import Embeddings
from openai import OpenAI

from app.core.config import settings

# 模块级缓存
_embeddings: "DashScopeEmbeddings | None" = None


class DashScopeEmbeddings(Embeddings):
    """基于 openai 客户端的文本嵌入，兼容 LangChain Embeddings 接口。

    内部调用 openai 兼容接口的 embeddings.create，显式携带 dimensions，
    保证维度与配置一致（qwen3.7-text-embedding-flash 实测上限 1024）。
    """

    def __init__(self) -> None:
        self._client = OpenAI(
            api_key=settings.api_key,
            base_url=settings.OPENAI_API_BASE,
        )
        self.model = settings.EMBEDDING_MODEL
        self.dimensions = settings.EMBEDDING_DIM

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """批量嵌入多个文本。

        Args:
            texts: 待嵌入文本列表。

        Returns:
            每个文本对应的向量列表。
        """
        res = self._client.embeddings.create(
            model=self.model, input=texts, dimensions=self.dimensions
        )
        return [d.embedding for d in res.data]

    def embed_query(self, text: str) -> list[float]:
        """嵌入单个查询文本（RAG 检索用）。

        Args:
            text: 查询文本。

        Returns:
            查询向量。
        """
        res = self._client.embeddings.create(
            model=self.model, input=[text], dimensions=self.dimensions
        )
        return res.data[0].embedding


def get_embeddings() -> DashScopeEmbeddings:
    """获取嵌入模型单例。

    返回自定义 DashScopeEmbeddings，向量维度由配置 EMBEDDING_DIM 控制。

    Returns:
        DashScopeEmbeddings 实例。
    """
    global _embeddings
    if _embeddings is None:
        _embeddings = DashScopeEmbeddings()
    return _embeddings
