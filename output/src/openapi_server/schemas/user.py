from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any

class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=6, example="password123")

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=6, example="password123")

class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: str
    updated_at: str

class ProfileUpdateRequest(BaseModel):
    password: str = Field(..., min_length=6, example="newpassword123")

class TokenResponse(BaseModel):
    token: str

class BaseResponse(BaseModel):
    code: int = 0
    msg: str = "success"
    data: Optional[Any] = None 