import sys
import importlib
import pytest

# 动态导入 Crypto
crypto_mod = importlib.import_module("openapi_server.core.crypto")
Crypto = crypto_mod.Crypto

def test_hash_and_verify():
    password = "testpassword123"
    hashed = Crypto.hash_password(password, rounds=6)  # 低轮数加快测试
    assert isinstance(hashed, str)
    assert hashed != password
    # 正确密码校验
    assert Crypto.verify_password(password, hashed)
    # 错误密码校验
    assert not Crypto.verify_password("wrongpassword", hashed)

def test_unicode_password():
    password = "密码123abc!@#"
    hashed = Crypto.hash_password(password, rounds=6)
    assert Crypto.verify_password(password, hashed)
    assert not Crypto.verify_password("密码123", hashed)

def test_invalid_hash():
    # 非法hash字符串
    with pytest.raises(ValueError):
        Crypto.verify_password("abc", "not_a_hash") 