from pydantic import BaseModel, Field
from typing import Optional, List

class RedeemRequest(BaseModel):
    code: str = Field(..., example="ABCD1234")

class CardCodeInfo(BaseModel):
    code: str
    value: int
    type: str
    is_used: bool
    used_by: Optional[int]
    used_at: Optional[str]
    created_at: str

class CardCodeLogInfo(BaseModel):
    code: str
    user_id: int
    used_at: str
    action: str

class CardCodeListResponse(BaseModel):
    codes: List[CardCodeInfo]

class CardCodeLogListResponse(BaseModel):
    logs: List[CardCodeLogInfo]

class CardCodeCreateRequest(BaseModel):
    count: int = Field(..., example=10)
    type: str = Field(..., example="both")
    value: int = Field(..., example=365) 