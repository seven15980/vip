from typing import Any, Optional, Dict

def success(data: Any = None, msg: str = "success", code: int = 0) -> Dict[str, Any]:
    return {"code": code, "message": msg, "data": data}

def error(msg: str = "error", code: int = 1, data: Any = None) -> Dict[str, Any]:
    return {"code": code, "message": msg, "data": data} 