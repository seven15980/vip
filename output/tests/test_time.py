import importlib
from datetime import datetime, timezone, timedelta
import time

mod = importlib.import_module("openapi_server.utils.time")
now_utc = mod.now_utc
format_iso = mod.format_iso
parse_iso = mod.parse_iso


def test_now_utc():
    t1 = now_utc()
    time.sleep(0.01)
    t2 = now_utc()
    assert t2 > t1
    assert t1.tzinfo == timezone.utc


def test_format_iso():
    dt = datetime(2024, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    s = format_iso(dt)
    assert s == "2024-01-02T03:04:05Z"


def test_parse_iso():
    s = "2024-01-02T03:04:05Z"
    dt = parse_iso(s)
    assert dt == datetime(2024, 1, 2, 3, 4, 5, tzinfo=timezone.utc)


def test_format_and_parse_roundtrip():
    now = now_utc()
    s = format_iso(now)
    dt2 = parse_iso(s)
    # 由于精度只到秒，允许1秒误差
    assert abs((now - dt2).total_seconds()) < 2


def test_parse_iso_invalid():
    try:
        parse_iso("not-a-date")
        assert False, "应抛出异常"
    except ValueError:
        pass 