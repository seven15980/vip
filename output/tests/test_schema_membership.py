import pytest
from pydantic import ValidationError
from openapi_server.schemas.membership import MembershipLocal, MembershipOnline, MembershipResponse

def test_membership_local():
    m = MembershipLocal(expire_at="2025-01-01T00:00:00Z")
    assert m.expire_at == "2025-01-01T00:00:00Z"
    with pytest.raises(ValidationError):
        MembershipLocal()

def test_membership_online():
    m = MembershipOnline(expire_at="2025-01-01T00:00:00Z", storage_total=20)
    assert m.storage_total == 20
    with pytest.raises(ValidationError):
        MembershipOnline(expire_at="2025-01-01T00:00:00Z")

def test_membership_response():
    resp = MembershipResponse(
        local={"expire_at": "2025-01-01T00:00:00Z"},
        online={"expire_at": "2025-01-01T00:00:00Z", "storage_total": 10}
    )
    assert resp.local.expire_at == "2025-01-01T00:00:00Z"
    assert resp.online.storage_total == 10
    # 可选字段
    resp2 = MembershipResponse(local=None, online=None)
    assert resp2.local is None
    assert resp2.online is None 