import importlib
import pytest
from fastapi import Request
from types import SimpleNamespace

# 构造假的 request
class DummyRequest:
    def __init__(self, token):
        self.headers = {"Authorization": f"Bearer {token}"}

# 动态导入 deps
deps_mod = importlib.import_module("openapi_server.deps")
get_current_user = deps_mod.get_current_user
get_current_admin = deps_mod.get_current_admin

# 动态导入 JWTUtil
jwt_mod = importlib.import_module("openapi_server.core.jwt")
JWTUtil = jwt_mod.JWTUtil

# 动态导入 APIException
exc_mod = importlib.import_module("openapi_server.core.exception")
APIException = exc_mod.APIException

class DummyDB:
    pass

def test_get_current_user_success():
    token = JWTUtil.create_access_token({"user_id": 42})
    req = DummyRequest(token)
    result = get_current_user(req, DummyDB())
    assert result["user_id"] == 42

def test_get_current_user_no_token():
    req = SimpleNamespace(headers={})
    with pytest.raises(APIException) as excinfo:
        get_current_user(req, DummyDB())
    assert excinfo.value.code == 401

def test_get_current_user_invalid_token():
    req = DummyRequest("invalid.token")
    with pytest.raises(APIException) as excinfo:
        get_current_user(req, DummyDB())
    assert excinfo.value.code == 401

def test_get_current_admin_success():
    token = JWTUtil.create_access_token({"admin_id": 99})
    req = DummyRequest(token)
    result = get_current_admin(req, DummyDB())
    assert result["admin_id"] == 99

def test_get_current_admin_no_token():
    req = SimpleNamespace(headers={})
    with pytest.raises(APIException) as excinfo:
        get_current_admin(req, DummyDB())
    assert excinfo.value.code == 401

def test_get_current_admin_invalid_token():
    req = DummyRequest("invalid.token")
    with pytest.raises(APIException) as excinfo:
        get_current_admin(req, DummyDB())
    assert excinfo.value.code == 401 