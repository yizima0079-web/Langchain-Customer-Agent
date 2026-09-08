"""知识库路由：上传、列表、删除（管理员）。"""
import os

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_db
from app.models.knowledge import KnowledgeFile
from app.models.user import User
from app.schemas.common import Response
from app.schemas.knowledge import KnowledgeFileOut
from app.services.knowledge_service import save_and_vectorize
from app.services.vectorstore import get_vectorstore

router = APIRouter(prefix="/knowledge", tags=["知识库"])


@router.post("", response_model=Response[KnowledgeFileOut], summary="上传知识库文件")
def upload_knowledge(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """上传知识库文件并完成解析、向量化入库。

    支持 txt / doc / docx / pdf / markdown 四种格式。
    """
    record = save_and_vectorize(file, db)
    return Response(data=KnowledgeFileOut.model_validate(record))


@router.get("", response_model=Response[list[KnowledgeFileOut]], summary="知识库文件列表")
def list_knowledge(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """返回全部知识库文件及其处理状态。"""
    items = db.query(KnowledgeFile).order_by(KnowledgeFile.id.desc()).all()
    return Response(data=[KnowledgeFileOut.model_validate(k) for k in items])


@router.delete("/{file_id}", summary="删除知识库文件")
def delete_knowledge(
    file_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """删除知识库文件，并同步清理向量库与本地文件。"""
    record = db.query(KnowledgeFile).filter(KnowledgeFile.id == file_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="文件不存在")

    # 清理向量库中该文件对应的向量块
    try:
        get_vectorstore().delete(where={"file_id": file_id})
    except Exception:
        pass  # 向量库清理失败不阻断删除流程

    # 清理本地文件
    try:
        if os.path.exists(record.file_path):
            os.remove(record.file_path)
    except OSError:
        pass

    db.delete(record)
    db.commit()
    return Response(data="已删除")
