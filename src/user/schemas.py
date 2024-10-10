from pydantic import BaseModel, Field, EmailStr


class UserBaseSchemas(BaseModel):
    """Стандартная схема пользователя"""
    username: str = Field(min_length=6, max_length=64)
    email: EmailStr


class MusicBaseSchemas(BaseModel):
    """Схема музыки у автора"""
    id: int
    title: str
    duration: float
    authors: list[str]


class UserSchemas(UserBaseSchemas):
    """Схема профиля пользователя"""
    avatar_url: str
    musics: list[MusicBaseSchemas]
    favorite_playlist: list[int]


class UserShortAuthorSchemas(BaseModel):
    """Модель минимальной информации о авторе"""
    username: str
