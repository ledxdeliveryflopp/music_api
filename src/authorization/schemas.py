from datetime import datetime

from pydantic import EmailStr, BaseModel


class LoginSchemas(BaseModel):
    """Схема логина"""
    email: EmailStr
    password: str


class TokenSchemas(BaseModel):
    """Схема токена"""
    token: str
    expire: datetime
