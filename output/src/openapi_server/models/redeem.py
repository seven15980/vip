from pydantic import BaseModel, Field
from typing import Optional

class RedeemCardRequest(BaseModel):
    code: str = Field(..., example="ABC123", description="兑换卡密")

class RedeemCardResponse(BaseModel):
    success: bool = Field(..., example=True, description="是否成功")
    msg: str = Field(..., example="兑换成功", description="返回信息")

class SuccessResponse(BaseModel):
    msg: str = Field(..., example="操作成功", description="返回信息") 