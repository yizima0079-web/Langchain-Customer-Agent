"""上传安全校验函数的单元测试。"""
import io

import pytest
from fastapi import HTTPException

from app.utils.uploads import read_limited, safe_subdir, validate_image_content


class _FakeFile:
    """模拟 UploadFile.file，仅提供 read(n) 接口。"""

    def __init__(self, data: bytes):
        self._io = io.BytesIO(data)

    def read(self, n: int) -> bytes:
        return self._io.read(n)


class _FakeUploadFile:
    """模拟 UploadFile，仅暴露 file 属性。"""

    def __init__(self, data: bytes):
        self.file = _FakeFile(data)


def test_read_limited_ok():
    assert read_limited(_FakeUploadFile(b"abc"), 1024) == b"abc"


def test_read_limited_exceed():
    """超过 max_size 抛 413。"""
    with pytest.raises(HTTPException) as e:
        read_limited(_FakeUploadFile(b"x" * 10), 5)
    assert e.value.status_code == 413


def test_validate_image_magic():
    """扩展名与内容魔数一致才通过，伪装文件拒绝。"""
    assert validate_image_content("jpg", b"\xff\xd8\xff" + b"rest")
    assert not validate_image_content("jpg", b"not-a-jpeg")
    assert validate_image_content("png", b"\x89PNG\r\n\x1a\n" + b"rest")
    assert validate_image_content("gif", b"GIF89a")
    assert not validate_image_content("gif", b"GIF88a")
    assert validate_image_content("webp", b"RIFF" + b"\x00\x00\x00\x00" + b"WEBP")


def test_safe_subdir():
    """仅接受纯子目录名，拒绝空串、上级目录与路径分隔符。"""
    assert safe_subdir("goods")
    assert not safe_subdir("")
    assert not safe_subdir(".")
    assert not safe_subdir("..")
    assert not safe_subdir("../evil")
    assert not safe_subdir("a/b")
    assert not safe_subdir("a\\b")
