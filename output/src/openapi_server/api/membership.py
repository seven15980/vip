from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from openapi_server.deps import get_current_user
from openapi_server.database import get_db
from openapi_server.crud import membership as crud_membership
from openapi_server.core.response import success, error

router = APIRouter()

@router.get("/membership")
def get_membership(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    # 查询本地会员
    local = crud_membership.get_membership_by_user(db, user_id=current_user.id, type="local")
    online = crud_membership.get_membership_by_user(db, user_id=current_user.id, type="online")
    data = {}
    if local:
        data["local"] = {"expire_at": local[0].expire_at.isoformat()}
    else:
        data["local"] = {"expire_at": "1970-01-01T00:00:00"}
    if online:
        data["online"] = {"expire_at": online[0].expire_at.isoformat(), "storage_total": online[0].storage_total}
    else:
        data["online"] = {"expire_at": "1970-01-01T00:00:00", "storage_total": 0}
    return success(data) 