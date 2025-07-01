from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from openapi_server.database import get_db
from openapi_server.schemas.admin import AdminLoginRequest, AdminMembershipRenewRequest
from openapi_server.core.response import success, error
from openapi_server.crud import admin as crud_admin
from openapi_server.core.crypto import verify_password
from openapi_server.core.jwt import create_access_token
from openapi_server.deps import get_current_admin
from openapi_server.schemas.card_code import CardCodeCreateRequest
from openapi_server.utils.card_code import batch_generate_card_codes
from openapi_server.crud import card_code as crud_card_code
from openapi_server.crud import card_code_log as crud_card_code_log
from openapi_server.crud import membership as crud_membership
from openapi_server.crud import user as crud_user
import datetime
from sqlalchemy import text

router = APIRouter()

@router.post("/admin/login")
def admin_login(data: AdminLoginRequest, db: Session = Depends(get_db)):
    admin = crud_admin.get_admin_by_username(db, data.username)
    if not admin or not verify_password(data.password, admin.password_hash):
        return error("账号或密码错误", code=401)
    token = create_access_token({"admin_id": admin.id})
    return success({"token": token})

@router.post("/admin/card-codes")
def batch_create_card_codes(data: CardCodeCreateRequest, current_admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    codes = batch_generate_card_codes(data.count)
    created = []
    for code in codes:
        card = crud_card_code.create_card_code(db, code=code, value=data.value, type=data.type)
        created.append({"code": card.code, "value": card.value, "type": card.type, "created_at": card.created_at.isoformat()})
    return success(created)

@router.get("/admin/card-codes")
def list_card_codes(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), current_admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    skip = (page - 1) * page_size
    total = db.query(crud_card_code.CardCode).count()
    items = crud_card_code.list_card_codes(db, skip=skip, limit=page_size)
    data = []
    for card in items:
        data.append({
            "code": card.code,
            "value": card.value,
            "type": card.type,
            "is_used": card.is_used,
            "used_by": card.used_by,
            "used_at": card.used_at.isoformat() if card.used_at else None,
            "created_at": card.created_at.isoformat() if card.created_at else None
        })
    return success({
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": data
    })

@router.get("/admin/card-codes/{code}/logs")
def get_card_code_logs(code: str, current_admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    logs = crud_card_code_log.list_logs_by_code(db, code)
    data = []
    for log in logs:
        data.append({
            "code": log.code,
            "user_id": log.user_id,
            "used_at": log.used_at.isoformat() if log.used_at else None,
            "action": log.action
        })
    return success(data)

@router.get("/admin/memberships")
def list_memberships(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), current_admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    skip = (page - 1) * page_size
    # 查询总数
    total = db.execute(text("SELECT COUNT(*) FROM v_user_membership")).scalar()
    # 查询分页数据
    result = db.execute(text(f"SELECT * FROM v_user_membership LIMIT :limit OFFSET :offset"), {"limit": page_size, "offset": skip})
    items = result.fetchall()
    columns = result.keys()
    data = [dict(zip(columns, row)) for row in items]
    return success({
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": data
    })

@router.get("/admin/memberships/{user_id}")
def get_membership_detail(user_id: int, current_admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    memberships = crud_membership.get_membership_by_user(db, user_id)
    data = []
    for m in memberships:
        data.append({
            "id": m.id,
            "user_id": m.user_id,
            "type": m.type,
            "expire_at": m.expire_at.isoformat() if m.expire_at else None,
            "storage_total": m.storage_total,
            "created_at": m.created_at.isoformat() if m.created_at else None,
            "updated_at": m.updated_at.isoformat() if m.updated_at else None
        })
    return success(data)

@router.post("/admin/memberships/{user_id}/renew")
def admin_renew_membership(user_id: int, data: AdminMembershipRenewRequest, current_admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    # 查找会员
    memberships = crud_membership.get_membership_by_user(db, user_id, type=data.type)
    import datetime
    now = datetime.datetime.utcnow()
    if memberships:
        m = memberships[0]
        # 延长到期时间
        if m.expire_at and m.expire_at > now:
            new_expire = m.expire_at + datetime.timedelta(days=30*data.months)
        else:
            new_expire = now + datetime.timedelta(days=30*data.months)
        update_data = {"expire_at": new_expire}
        if data.type == "online" and data.storage:
            update_data["storage_total"] = (m.storage_total or 0) + data.storage
        m = crud_membership.update_membership(db, m, **update_data)
    else:
        # 新建会员
        expire_at = now + datetime.timedelta(days=30*data.months)
        storage = data.storage if data.type == "online" else None
        m = crud_membership.create_membership(db, user_id=user_id, type=data.type, expire_at=expire_at, storage_total=storage)
    # 写入日志
    crud_card_code_log.create_card_code_log(db, code="后台续费", user_id=user_id, used_at=now, action=f"后台续费{data.type} {data.months}月 {data.storage if data.type=='online' else ''}")
    return success({"id": m.id, "user_id": m.user_id, "type": m.type, "expire_at": m.expire_at.isoformat(), "storage_total": m.storage_total})

@router.get("/admin/statistics")
def get_statistics(current_admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    user_count = db.query(crud_user.User).count()
    from openapi_server.crud.membership import Membership
    membership_count = db.query(Membership).count()
    from openapi_server.crud.card_code import CardCode
    card_code_used_count = db.query(CardCode).filter(CardCode.is_used == True).count()
    return success({
        "user_count": user_count,
        "membership_count": membership_count,
        "card_code_used_count": card_code_used_count
    }) 