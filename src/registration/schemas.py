from pydantic import Field, EmailStr, BaseModel


class UserBaseSchemas(BaseModel):
    """Стандартная схема пользователя"""
    username: str = Field(min_length=4, max_length=64)
    email: EmailStr


class UserCreateSchemas(UserBaseSchemas):
    """Схема создания пользователя"""
    password: str = Field(min_length=6, max_length=255)
