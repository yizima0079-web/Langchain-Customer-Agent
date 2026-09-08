"""密码哈希与 JWT 工具函数的单元测试。"""
from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    md5_hash,
    needs_rehash,
    verify_password,
)


def test_bcrypt_hash_and_verify():
    """bcrypt 哈希以 $2 开头，正确密码通过、错误密码拒绝。"""
    hashed = hash_password("123456")
    assert hashed.startswith("$2")
    assert verify_password("123456", hashed)
    assert not verify_password("wrong", hashed)


def test_legacy_md5_compat_verify():
    """历史 MD5 密码仍可校验，且标记为需升级。"""
    legacy = md5_hash("123456")
    assert needs_rehash(legacy)
    assert verify_password("123456", legacy)
    assert not verify_password("wrong", legacy)


def test_needs_rehash_only_for_md5():
    """bcrypt 哈希无需再升级。"""
    assert not needs_rehash(hash_password("123456"))


def test_verify_invalid_hash_returns_false():
    """非法哈希串不抛异常，返回 False。"""
    assert not verify_password("123456", "not-a-valid-hash")


def test_jwt_roundtrip():
    """令牌签发后可解析，sub 与签发主体一致。"""
    token = create_access_token(1)
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "1"


def test_decode_bad_token_returns_none():
    """伪造令牌解析失败返回 None，不抛异常。"""
    assert decode_token("bad.token.here") is None
