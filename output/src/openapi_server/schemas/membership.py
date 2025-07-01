from pydantic import BaseModel, Field
from typing import Optional

class MembershipLocal(BaseModel):
    expire_at: str = Field(..., example="2025-01-01T00:00:00Z")

class MembershipOnline(BaseModel):
    expire_at: str = Field(..., example="2025-01-01T00:00:00Z")
    storage_total: int = Field(..., example=20)

class MembershipResponse(BaseModel):
    local: Optional[MembershipLocal]
    online: Optional[MembershipOnline] 