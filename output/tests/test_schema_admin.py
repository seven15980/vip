import pytest
from pydantic import ValidationError
from openapi_server.schemas.admin import (
    AdminLoginRequest, AdminCardCodeGenRequest, AdminMembershipRenewRequest, AdminStatisticsResponse
)

def test_admin_login_request():
    req = AdminLoginRequest(username="admin", password="admin123")
    assert req.username == "admin"
    with pytest.raises(ValidationError):
        AdminLoginRequest(username="admin")

def test_admin_card_code_gen_request():
    req = AdminCardCodeGenRequest(count=5, type="online", value=365)
    assert req.count == 5
    with pytest.raises(ValidationError):
        AdminCardCodeGenRequest(count=1, type="local")

def test_admin_membership_renew_request():
    req = AdminMembershipRenewRequest(type="online", months=6, storage=20)
    assert req.months == 6
    with pytest.raises(ValidationError):
        AdminMembershipRenewRequest(type="local", months=1)

def test_admin_statistics_response():
    resp = AdminStatisticsResponse(user_count=10, membership_count=5, card_code_used_count=3)
    assert resp.user_count == 10
    assert resp.card_code_used_count == 3 