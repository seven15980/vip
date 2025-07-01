from datetime import datetime, timezone
from typing import Optional

ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def now_utc() -> datetime:
    """
    获取当前UTC时间（datetime对象，带时区信息）。
    """
    return datetime.now(timezone.utc)


def format_iso(dt: datetime) -> str:
    """
    将datetime对象格式化为ISO 8601字符串（UTC，Z结尾）。
    """
    return dt.astimezone(timezone.utc).strftime(ISO_FORMAT)


def parse_iso(s: str) -> datetime:
    """
    将ISO 8601字符串解析为datetime对象（UTC）。
    """
    return datetime.strptime(s, ISO_FORMAT).replace(tzinfo=timezone.utc) 