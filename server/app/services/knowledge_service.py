"""知识库业务编排：上传 → 落盘 → 解析 → 切分 → 向量化 → 更新状态。"""
import os
import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.knowledge import KnowledgeFile
from app.services.document_loader import SUPPORTED_EXTENSIONS, load_documents, split_documents
from app.services.vectorstore import get_vectorstore
from app.utils.uploads import read_limited

# 知识库文件落盘子目录（位于 F:/uploads14/knowledge）
KNOWLEDGE_DIR = os.path.join(settings.UPLOAD_DIR, "knowledge")
# 知识库文件大小上限（20MB）
MAX_KNOWLEDGE_SIZE = 20 * 1024 * 1024


def _ensure_dir() -> None:
    """确保知识库目录存在。"""
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)


def save_and_vectorize(file: UploadFile, db: Session) -> KnowledgeFile:
    """保存上传文件并完成向量化入库。

    流程：
        1. 校验扩展名是否支持；
        2. 读取文件内容并落盘到 KNOWLEDGE_DIR；
        3. 写入 knowledge_file 记录（状态=待处理）；
        4. 解析 → 切分 → 写入 Chroma；
        5. 更新记录状态（成功/失败）。

    Args:
        file: 上传的文件对象。
        db: 数据库会话。

    Returns:
        处理后的 KnowledgeFile 记录。

    Raises:
        HTTPException: 文件类型不支持（400）。
    """
    filename = file.filename or "unknown"
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in ("md", "markdown"):
        ext = "markdown"  # 统一 Markdown 类型标识
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型: {ext}，仅支持 txt / doc / pdf / markdown",
        )

    # 落盘：使用 uuid 重命名，避免中文/重名冲突
    _ensure_dir()
    # 分块读取并限制大小，避免大文件整读占用内存
    content = read_limited(file, MAX_KNOWLEDGE_SIZE)
    store_name = f"{uuid.uuid4().hex}.{ext}"
    store_path = os.path.join(KNOWLEDGE_DIR, store_name)
    with open(store_path, "wb") as f:
        f.write(content)

    # 建立记录（状态=待处理）
    record = KnowledgeFile(
        filename=filename,
        file_type=ext,
        file_path=store_path,
        size=len(content),
        status=0,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    # 解析 + 切分 + 向量化
    try:
        docs = load_documents(store_path, ext)
        chunks = split_documents(docs)
        if not chunks:
            raise ValueError("文档切分后无有效文本块")
        # 为每个文本块打上 file_id 标记，便于删除文件时同步清理向量
        for chunk in chunks:
            chunk.metadata["file_id"] = record.id
        get_vectorstore().add_documents(chunks)
        record.status = 1
        record.chunk_count = len(chunks)
    except Exception as exc:  # noqa: BLE001 - 记录失败原因并落库
        record.status = 2
        record.error_msg = str(exc)[:500]

    db.commit()
    db.refresh(record)
    return record
