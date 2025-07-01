import os
import importlib
import sys
import pytest

def test_default_settings(monkeypatch):
    # 移除环境变量，测试默认值
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    monkeypatch.delenv("JWT_ALGORITHM", raising=False)
    monkeypatch.delenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", raising=False)
    monkeypatch.delenv("BCRYPT_ROUNDS", raising=False)

    # 重新导入 config
    if "output.src.openapi_server.config" in sys.modules:
        del sys.modules["output.src.openapi_server.config"]
    config = importlib.import_module("output.src.openapi_server.config")
    settings = config.settings

    assert settings.SQLALCHEMY_DATABASE_URL == "sqlite:///./test.db"
    assert settings.JWT_SECRET_KEY == "your-secret-key"
    assert settings.JWT_ALGORITHM == "HS256"
    assert settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES == 60 * 24
    assert settings.BCRYPT_ROUNDS == 12

def test_env_override(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./prod.db")
    monkeypatch.setenv("JWT_SECRET_KEY", "env-secret")
    monkeypatch.setenv("JWT_ALGORITHM", "HS512")
    monkeypatch.setenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    monkeypatch.setenv("BCRYPT_ROUNDS", "8")

    if "output.src.openapi_server.config" in sys.modules:
        del sys.modules["output.src.openapi_server.config"]
    config = importlib.import_module("output.src.openapi_server.config")
    settings = config.settings

    assert settings.SQLALCHEMY_DATABASE_URL == "sqlite:///./prod.db"
    assert settings.JWT_SECRET_KEY == "env-secret"
    assert settings.JWT_ALGORITHM == "HS512"
    assert settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES == 30
    assert settings.BCRYPT_ROUNDS == 8 