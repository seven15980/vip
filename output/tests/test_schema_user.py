import pytest
from pydantic import ValidationError
from openapi_server.schemas.user import (
    RegisterRequest, LoginRequest, UserProfileResponse, ProfileUpdateRequest, TokenResponse, BaseResponse
)

def test_register_request_valid():
    data = {"email": "a@b.com", "password": "abcdef"}
    req = RegisterRequest(**data)
    assert req.email == "a@b.com"
    assert req.password == "abcdef"

def test_register_request_invalid_email():
    with pytest.raises(ValidationError):
        RegisterRequest(email="not-an-email", password="abcdef")

def test_register_request_short_password():
    with pytest.raises(ValidationError):
        RegisterRequest(email="a@b.com", password="123")

def test_login_request():
    req = LoginRequest(email="a@b.com", password="abcdef")
    assert req.email == "a@b.com"

def test_user_profile_response():
    resp = UserProfileResponse(id=1, email="a@b.com", is_active=True, created_at="2024-01-01T00:00:00Z", updated_at="2024-01-01T00:00:00Z")
    assert resp.id == 1
    assert resp.is_active is True

def test_profile_update_request():
    req = ProfileUpdateRequest(password="newpass123")
    assert req.password == "newpass123"
    with pytest.raises(ValidationError):
        ProfileUpdateRequest(password="123")

def test_token_response():
    resp = TokenResponse(token="abc.def.ghi")
    assert resp.token == "abc.def.ghi"

def test_base_response():
    resp = BaseResponse(code=0, msg="ok", data={"x": 1})
    assert resp.code == 0
    assert resp.msg == "ok"
    assert resp.data == {"x": 1} 