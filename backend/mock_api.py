from fastapi import FastAPI, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. 用户相关
@app.post("/api/register")
async def register(user: dict):
    return {"message": "注册成功"}

@app.post("/api/login")
async def login(user: dict):
    return {"token": "mock_token_1_123456", "message": "登录成功"}

@app.get("/api/profile")
async def profile(authorization: Optional[str] = Header(None)):
    return {"id": 1, "email": "test@example.com", "created_at": "2024-01-01T00:00:00Z"}

# 2. 会员相关
@app.get("/api/membership")
async def membership(authorization: Optional[str] = Header(None)):
    return {
        "local": {"expire_at": "2025-12-31T23:59:59Z"},
        "online": {"expire_at": "2025-06-30T23:59:59Z", "storage_total": 20}
    }

@app.get("/api/admin/memberships")
async def admin_memberships(authorization: Optional[str] = Header(None)):
    return [
        {
            "user_id": 1,
            "email": "test",
            "local_expire": "2025-12-31T23:59:59Z",
            "online_expire": "2025-06-30T23:59:59Z",
            "storage_total": 20,
            "created_at": "2024-01-01T00:00:00Z",
            "last_login": "2024-01-15T10:30:00Z",
        }
    ]

@app.post("/api/admin/memberships/{user_id}/renew")
async def renew_membership(user_id: int, data: dict, authorization: Optional[str] = Header(None)):
    return {"message": f"成功为用户{user_id}续费{data.get('type')}会员{data.get('months')}个月"}

# 3. 卡密相关
@app.post("/api/redeem")
async def redeem(data: dict, authorization: Optional[str] = Header(None)):
    return {"message": "兑换成功"}

@app.get("/api/admin/card-codes")
async def card_codes(authorization: Optional[str] = Header(None)):
    return [
        {
            "code": "ABCD1234",
            "type": "local",
            "value": 30,
            "status": "unused",
            "created_at": "2024-01-10T10:00:00Z",
            "used_at": None,
            "used_by": None,
        }
    ]

@app.post("/api/admin/card-codes")
async def generate_card_codes(data: dict, authorization: Optional[str] = Header(None)):
    return {"message": f"成功生成{data.get('count', 1)}个卡密", "codes": ["MOCKCODE1", "MOCKCODE2"]}

# 4. 通知相关
@app.get("/api/notifications")
async def notifications(authorization: Optional[str] = Header(None)):
    return [
        {
            "id": 1,
            "title": "欢迎使用会员系统",
            "content": "感谢您注册我们的会员系统！",
            "type": "info",
            "is_read": False,
            "created_at": "2024-01-15T10:00:00Z",
        }
    ]

@app.put("/api/notifications/{id}/read")
async def read_notification(id: int, authorization: Optional[str] = Header(None)):
    return {"message": "已读"}

# 5. 统计相关
@app.get("/api/admin/statistics")
async def statistics(authorization: Optional[str] = Header(None)):
    return {
        "total_users": 1248,
        "active_members": 892,
        "total_cards": 500,
        "used_cards": 267,
        "revenue_this_month": 15680,
        "new_users_this_week": 23,
    }

@app.post("/api/admin/login")
async def admin_login(user: dict):
    return {"token": "admin_token_1_123456", "message": "登录成功"} 