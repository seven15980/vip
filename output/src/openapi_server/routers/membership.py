from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from ..models.membership import MembershipStatusResponse, MembershipStatusLocal, MembershipStatusOnline
from ..deps import get_current_user
from ..database import get_db
from ..crud import membership as crud_membership

router = APIRouter(
    prefix="/membership",
    tags=["membership"]
)

@router.get("/", response_model=MembershipStatusResponse)
def get_membership(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    local = crud_membership.get_membership_by_user(db, user_id=current_user.id, type="local")
    online = crud_membership.get_membership_by_user(db, user_id=current_user.id, type="online")
    data = MembershipStatusResponse(
        local=MembershipStatusLocal(
            expire_at=local[0].expire_at if local else None
        ),
        online=MembershipStatusOnline(
            expire_at=online[0].expire_at if online else None,
            storage_total=online[0].storage_total if online and online[0].storage_total else 0
        )
    )
    return data 