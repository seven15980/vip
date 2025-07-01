from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.admin import (
    AdminLoginRequest,
    AdminLoginResponse,
    CardCodeCreateRequest,
    CardCodeOut,
    CardCodeLogOut,
    MembershipOut,
    MembershipRenewRequest,
    MembershipRenewResponse,
    StatisticsResponse,
    SuccessResponse,
)
from ..database import get_db
from ..core.response import success, error
from ..crud import admin as crud_admin
from ..core.crypto import verify_password
from ..core.jwt import create_access_token
from ..deps import get_current_admin
from ..crud import card_code as crud_card_code
from ..crud import card_code_log as crud_card_code_log
from ..crud import membership as crud_membership
from ..crud import user as crud_user
from sqlalchemy import text
import datetime

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.post("/login", response_model=AdminLoginResponse)
def admin_login(
    data: AdminLoginRequest = Body(...),
    db: Session = Depends(get_db)
):
    admin = crud_admin.get_admin_by_username(db, data.username)
    if not admin or not verify_password(data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="账号或密码错误")
    token = create_access_token({"admin_id": admin.id})
    return AdminLoginResponse(token=token, admin_id=admin.id)

@router.post("/card-codes", response_model=List[CardCodeOut])
def batch_create_card_codes(
    data: CardCodeCreateRequest = Body(...),
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from ..utils.card_code import batch_generate_card_codes
    codes = batch_generate_card_codes(data.count)
    created = []
    for code in codes:
        card = crud_card_code.create_card_code(db, code=code, value=data.value, type=data.type)
        created.append(CardCodeOut.from_orm(card))
    return created

@router.get("/card-codes", response_model=List[CardCodeOut])
def list_card_codes(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    items = crud_card_code.list_card_codes(db, skip=skip, limit=page_size)
    return [CardCodeOut.from_orm(card) for card in items]

@router.get("/card-codes/{code}/logs", response_model=List[CardCodeLogOut])
def get_card_code_logs(
    code: str,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    logs = crud_card_code_log.list_logs_by_code(db, code)
    return [CardCodeLogOut.from_orm(log) for log in logs]

@router.get("/memberships", response_model=List[MembershipOut])
def list_memberships(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    result = db.execute(text(f"SELECT * FROM v_user_membership LIMIT :limit OFFSET :offset"), {"limit": page_size, "offset": skip})
    items = result.fetchall()
    columns = result.keys()
    return [MembershipOut(**dict(zip(columns, row))) for row in items]

@router.get("/memberships/{user_id}", response_model=List[MembershipOut])
def get_membership_detail(
    user_id: int,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    memberships = crud_membership.get_membership_by_user(db, user_id)
    return [MembershipOut.from_orm(m) for m in memberships]

@router.post("/memberships/{user_id}/renew", response_model=MembershipRenewResponse)
def admin_renew_membership(
    user_id: int,
    data: MembershipRenewRequest = Body(...),
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    memberships = crud_membership.get_membership_by_user(db, user_id, type=data.type)
    now = datetime.datetime.utcnow()
    if memberships:
        m = memberships[0]
        if m.expire_at and m.expire_at > now:
            new_expire = m.expire_at + datetime.timedelta(days=30*data.months)
        else:
            new_expire = now + datetime.timedelta(days=30*data.months)
        update_data = {"expire_at": new_expire}
        if data.type == "online" and data.storage:
            update_data["storage_total"] = (m.storage_total or 0) + data.storage
        m = crud_membership.update_membership(db, m, **update_data)
    else:
        expire_at = now + datetime.timedelta(days=30*data.months)
        storage = data.storage if data.type == "online" else None
        m = crud_membership.create_membership(db, user_id=user_id, type=data.type, expire_at=expire_at, storage_total=storage)
    crud_card_code_log.create_card_code_log(db, code="后台续费", user_id=user_id, used_at=now, action=f"后台续费{data.type} {data.months}月 {data.storage if data.type=='online' else ''}")
    return MembershipRenewResponse(id=m.id, user_id=m.user_id, type=m.type, expire_at=m.expire_at, storage_total=m.storage_total)

@router.get("/statistics", response_model=StatisticsResponse)
def get_statistics(
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user_count = db.query(crud_user.User).count()
    from ..crud.membership import Membership
    membership_count = db.query(Membership).count()
    from ..crud.card_code import CardCode
    card_code_used_count = db.query(CardCode).filter(CardCode.is_used == True).count()
    return StatisticsResponse(
        user_count=user_count,
        membership_count=membership_count,
        card_code_used_count=card_code_used_count
    ) 