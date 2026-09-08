"""RAG 检索增强生成：向量检索相关文档 + LLM 生成回答。

使用 LangChain 1.x 的 LCEL 组合式写法（旧版 langchain.chains 链已移除）。
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.services.llm import get_llm
from app.services.vectorstore import get_vectorstore

# 检索返回的相关文档块数量
RETRIEVE_TOP_K = 4

# 客服系统提示词：限定回答范围、基于上下文、友好简洁
SYSTEM_PROMPT = (
    "你是本商城专业的智能客服助手，请严格根据下方提供的【知识库上下文】回答用户问题。\n"
    "要求：\n"
    "1. 优先使用上下文中的信息作答，不得编造知识库以外的内容；\n"
    "2. 若上下文没有相关信息，请礼貌说明暂未找到相关答案，并建议转人工客服；\n"
    "3. 回答简洁、准确、友好，使用中文。\n\n"
    "【知识库上下文】\n{context}"
)


def _format_docs(docs: list) -> str:
    """将检索到的文档块拼接为一段可读文本。"""
    return "\n\n".join(doc.page_content for doc in docs)


def ask(question: str) -> tuple[str, list[str]]:
    """执行一次 RAG 问答。

    流程：向量化问题 → Chroma 检索 top_k 文档块 →
         拼接上下文与提示词 → qwen 生成回答。

    Args:
        question: 用户提问。

    Returns:
        (回答文本, 命中的知识库来源片段列表)。
    """
    llm = get_llm()
    retriever = get_vectorstore().as_retriever(search_kwargs={"k": RETRIEVE_TOP_K})

    # 先检索，拿到来源片段供前端展示
    docs = retriever.invoke(question)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{input}"),
        ]
    )
    # LCEL 链路：提示词 → 大模型 → 纯文本输出
    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({"input": question, "context": _format_docs(docs)})
    # 截取来源片段前 200 字，便于前端展示参考
    sources = [doc.page_content[:200] for doc in docs]
    return answer, sources


def stream(question: str):
    """执行 RAG 问答并逐块返回模型输出。"""
    llm = get_llm()
    retriever = get_vectorstore().as_retriever(search_kwargs={"k": RETRIEVE_TOP_K})
    docs = retriever.invoke(question)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{input}"),
        ]
    )
    chain = prompt | llm | StrOutputParser()
    return chain.stream({"input": question, "context": _format_docs(docs)})
