import importlib

def test_success():
    resp_mod = importlib.import_module("openapi_server.core.response")
    data = {"a": 1}
    res = resp_mod.success(data, msg="ok", code=0)
    assert res["code"] == 0
    assert res["msg"] == "ok"
    assert res["data"] == data

def test_error():
    resp_mod = importlib.import_module("openapi_server.core.response")
    res = resp_mod.error(msg="fail", code=123, data=None)
    assert res["code"] == 123
    assert res["msg"] == "fail"
    assert res["data"] is None 