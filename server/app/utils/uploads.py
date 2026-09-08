"""上传文件安全校验工具：分块限流读取、内容魔数校验、子目录防穿越。"""
from fastapi import HTTPException, UploadFile


def read_limited(file: UploadFile, max_size: int) -> bytes:
    """分块读取上传文件，超过 max_size 字节立即拒绝，避免大文件整读占用内存。

    Args:
        file: 上传文件对象。
        max_size: 允许的最大字节数。

    Returns:
        文件完整内容。

    Raises:
        HTTPException: 文件超过大小限制（413）。
    """
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = file.file.read(1024 * 1024)  # 每次读 1MB
        if not chunk:
            break
        total += len(chunk)
        if total > max_size:
            raise HTTPException(
                status_code=413,
                detail=f"文件超过大小限制（{max_size // 1024 // 1024}MB）",
            )
        chunks.append(chunk)
    return b"".join(chunks)


def validate_image_content(ext: str, data: bytes) -> bool:
    """校验图片内容魔数与扩展名是否一致，防止伪装文件。

    Args:
        ext: 文件扩展名（小写）。
        data: 文件内容。

    Returns:
        内容与扩展名是否匹配。
    """
    if ext in ("jpg", "jpeg"):
        return data[:3] == b"\xff\xd8\xff"
    if ext == "png":
        return data[:8] == b"\x89PNG\r\n\x1a\n"
    if ext == "gif":
        return data[:6] in (b"GIF87a", b"GIF89a")
    if ext == "webp":
        return len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    return True


def safe_subdir(name: str) -> bool:
    """校验子目录名是否安全（非空、不含路径分隔符与上级目录），防止路径穿越。"""
    return bool(name) and name not in (".", "..") and "/" not in name and "\\" not in name
