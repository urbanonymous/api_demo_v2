from pydantic import BaseModel
from typing import Optional

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str
    token_type: str = "Bearer" # Case insensitive by spec
    iss: str = "API DEMO V2"
    active: bool = True
    exp: Optional[int, None] = None
