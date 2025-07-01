import importlib
import pytest
from fastapi import Request, HTTPException
from starlette.responses import Response
import types

exc_mod = importlib.import_module("openapi_server.core.exception")
APIException = exc_mod.APIException
api_exception_handler = exc_mod.api_exception_handler
http_exception_handler = exc_mod.http_exception_handler
generic_exception_handler = exc_mod.generic_exception_handler

class DummyRequest:
    pass

@pytest.mark.asyncio
async def test_api_exception_handler():
    exc = APIException(msg="test error", code=99, data={"x":1})
    req = DummyRequest()
    resp = await api_exception_handler(req, exc)
    assert resp.status_code == 200
    assert resp.body
    assert b'test error' in resp.body

@pytest.mark.asyncio
async def test_http_exception_handler():
    exc = HTTPException(status_code=404, detail="not found")
    req = DummyRequest()
    resp = await http_exception_handler(req, exc)
    assert resp.status_code == 404
    assert b'not found' in resp.body

@pytest.mark.asyncio
async def test_generic_exception_handler():
    exc = Exception("unknown")
    req = DummyRequest()
    resp = await generic_exception_handler(req, exc)
    assert resp.status_code == 500
    assert b'unknown' in resp.body 