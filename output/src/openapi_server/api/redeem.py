from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from openapi_server.deps import get_current_user
from openapi_server.database import get_db
from openapi_server.crud import card_code as crud_card_code, membership as crud_membership, card_code_log as crud_card_code_log
from openapi_server.core.response import success, error
import datetime

router = APIRouter()

@router.post("/redeem")
def redeem_card(data: dict, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    code = data.get("code")
    if not code:
        return error("卡密不能为空", code=400)
    card = crud_card_code.get_card_code_by_code(db, code)
    if not card or card.is_used:
        return error("卡密无效或已使用", code=400)
    # 校验卡密类型
    if card.type not in ("local", "online", "both"):
        return error("卡密类型错误", code=400)
    now = datetime.datetime.utcnow()
    # 兑换逻辑
    if card.type in ("local", "both"):
        # 本地会员：延长一年
        local = crud_membership.get_membership_by_user(db, current_user.id, type="local")
        expire = now + datetime.timedelta(days=365)
        if local:
            expire = max(local[0].expire_at, now) + datetime.timedelta(days=365)
            crud_membership.update_membership(db, local[0], expire_at=expire)
        else:
            crud_membership.create_membership(db, user_id=current_user.id, type="local", expire_at=expire)
        action = "充值本地会员一年"
    elif card.type == "online":
        # 线上会员：增加10G和一年时长
        online = crud_membership.get_membership_by_user(db, current_user.id, type="online")
        expire = now + datetime.timedelta(days=365)
        if online:
            expire = max(online[0].expire_at, now) + datetime.timedelta(days=365)
            storage = (online[0].storage_total or 0) + 10
            crud_membership.update_membership(db, online[0], expire_at=expire, storage_total=storage)
        else:
            storage = 10
            crud_membership.create_membership(db, user_id=current_user.id, type="online", expire_at=expire, storage_total=storage)
        action = "充值线上会员10G/年"
    # 更新卡密为已用
    crud_card_code.update_card_code(db, card, is_used=True, used_by=current_user.id, used_at=now)
    # 写入日志
    crud_card_code_log.create_card_code_log(db, code=code, user_id=current_user.id, used_at=now, action=action)
    return success({"msg": "兑换成功"}) 