"""应用配置的单元测试：JWT 密钥校验与连接串编码。"""
import pytest

from app.core.config import Settings


def test_weak_jwt_secret_rejected_in_prod():
    """生产环境（DEBUG=False）使用弱密钥必须报错。"""
    with pytest.raises(ValueError):
        Settings(JWT_SECRET="123456", DEBUG=False)


def test_weak_jwt_secret_allowed_in_debug():
    """开发环境（DEBUG=True）弱密钥仅告警，可正常实例化。"""
    s = Settings(JWT_SECRET="secret", DEBUG=True)
    assert s.JWT_SECRET == "secret"


def test_database_url_encodes_password():
    """连接串密码含特殊字符时做 URL 编码，避免解析异常。"""
    s = Settings(MYSQL_PASSWORD="p@ss/word")
    assert "p%40ss%2Fword" in s.database_url
