import sys
import importlib
import pytest
from datetime import timedelta
import time

jwt_mod = importlib.import_module("openapi_server.core.jwt")
JWTUtil = jwt_mod.JWTUtil


def test_create_and_decode_token():
    data = {"user_id": 123, "role": "user"}
    token = JWTUtil.create_access_token(data, expires_delta=timedelta(seconds=10))
    assert isinstance(token, str)
    payload = JWTUtil.decode_token(token)
    assert payload["user_id"] == 123
    assert payload["role"] == "user"
    assert "exp" in payload


def test_expired_token():
    data = {"user_id": 1}
    token = JWTUtil.create_access_token(data, expires_delta=timedelta(seconds=1))
    time.sleep(2)
    with pytest.raises(Exception) as excinfo:
        JWTUtil.decode_token(token)
    assert excinfo.type.__name__ in ("ExpiredSignatureError", "JWTError")


def test_invalid_token():
    # 随机字符串不是合法token
    with pytest.raises(Exception):
        JWTUtil.decode_token("not.a.jwt.token") 