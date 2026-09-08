"""文件上传路由（图片统一存 F:/uploads14）。"""
import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.config import settings
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.common import Response
from app.utils.uploads import read_limited, safe_subdir, validate_image_content

router = APIRouter(prefix="/upload", tags=["文件上传"])

# 允许的图片格式
ALLOWED_IMAGE = {"jpg", "jpeg", "png", "gif", "webp"}
# 图片上传大小上限（10MB）
MAX_IMAGE_SIZE = 10 * 1024 * 1024


@router.post("", summary="上传图片")
def upload_image(
    file: UploadFile = File(...),
    category: str = "common",
    _: User = Depends(get_current_user),
):
    """上传图片到统一上传目录，返回可访问的相对 URL。

    Args:
        file: 上传的图片文件。
        category: 子目录分类（如 product/avatar）。
    """
    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_IMAGE:
        raise HTTPException(status_code=400, detail="仅支持 jpg/jpeg/png/gif/webp 图片")
    if not safe_subdir(category):
        raise HTTPException(status_code=400, detail="非法的分类目录")

    # 分块读取并限制大小，避免大文件整读占用内存
    content = read_limited(file, MAX_IMAGE_SIZE)
    # 校验内容魔数，防止伪装文件
    if not validate_image_content(ext, content):
        raise HTTPException(status_code=400, detail="文件内容与扩展名不符")

    subdir = os.path.join(settings.UPLOAD_DIR, category)
    os.makedirs(subdir, exist_ok=True)

    store_name = f"{uuid.uuid4().hex}.{ext}"
    store_path = os.path.join(subdir, store_name)
    with open(store_path, "wb") as f:
        f.write(content)

    # 返回相对路径，前端/小程序拼接后端 baseURL 后访问
    url = f"/uploads14/{category}/{store_name}"
    return Response(data={"url": url, "filename": filename})
