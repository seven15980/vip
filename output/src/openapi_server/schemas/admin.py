from pydantic import BaseModel, Field
from typing import Optional, List

class AdminLoginRequest(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., example="admin123")

class AdminCardCodeGenRequest(BaseModel):
    count: int = Field(..., example=10)
    type: str = Field(..., example="both")
    value: int = Field(..., example=365)

class AdminMembershipRenewRequest(BaseModel):
    type: str = Field(..., example="online")
    months: int = Field(..., example=12)
    storage: int = Field(..., example=10)

class AdminStatisticsResponse(BaseModel):
    user_count: int
    membership_count: int
    card_code_used_count: int
    # 可根据实际统计项扩展 