import pytest
from pydantic import ValidationError
from openapi_server.schemas.card_code import (
    RedeemRequest, CardCodeInfo, CardCodeLogInfo, CardCodeListResponse, CardCodeLogListResponse
)

def test_redeem_request():
    req = RedeemRequest(code="ABCD1234")
    assert req.code == "ABCD1234"
    with pytest.raises(ValidationError):
        RedeemRequest()

def test_card_code_info():
    info = CardCodeInfo(
        code="CODE1", value=365, type="local", is_used=False,
        used_by=None, used_at=None, created_at="2024-01-01T00:00:00Z"
    )
    assert info.code == "CODE1"
    assert info.is_used is False

def test_card_code_log_info():
    log = CardCodeLogInfo(
        code="CODE1", user_id=1, used_at="2024-01-01T00:00:00Z", action="兑换"
    )
    assert log.action == "兑换"

def test_card_code_list_response():
    resp = CardCodeListResponse(codes=[
        {"code": "C1", "value": 365, "type": "local", "is_used": False, "used_by": None, "used_at": None, "created_at": "2024-01-01T00:00:00Z"}
    ])
    assert len(resp.codes) == 1
    assert resp.codes[0].code == "C1"

def test_card_code_log_list_response():
    resp = CardCodeLogListResponse(logs=[
        {"code": "C1", "user_id": 1, "used_at": "2024-01-01T00:00:00Z", "action": "兑换"}
    ])
    assert len(resp.logs) == 1
    assert resp.logs[0].user_id == 1 