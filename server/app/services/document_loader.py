"""知识库文档解析与切分。

支持四种格式：txt / doc(docx) / pdf / markdown。
"""
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 支持的文件扩展名集合
SUPPORTED_EXTENSIONS = {"txt", "md", "markdown", "pdf", "doc", "docx"}

# 文本切分参数
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def load_documents(file_path: str, file_type: str) -> list:
    """根据文件类型加载并解析文档为 Document 列表。

    Args:
        file_path: 本地文件路径。
        file_type: 文件类型（扩展名）。

    Returns:
        langchain Document 列表。

    Raises:
        ValueError: 文件类型不支持或解析失败。
    """
    ext = file_type.lower()
    if ext in ("txt", "md", "markdown"):
        # 纯文本与 Markdown 均按文本读取
        loader = TextLoader(file_path, encoding="utf-8")
    elif ext == "pdf":
        loader = PyPDFLoader(file_path)
    elif ext in ("doc", "docx"):
        # python-docx 解析（老式 .doc 二进制格式可能失败，需转换为 .docx）
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError(f"不支持的文件类型: {file_type}")

    docs = loader.load()
    if not docs:
        raise ValueError("文档解析后无有效内容")
    return docs


def split_documents(docs: list) -> list:
    """将文档按固定大小切分为文本块。

    Args:
        docs: 原始 Document 列表。

    Returns:
        切分后的 Document 列表。
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(docs)
