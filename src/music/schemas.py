from pydantic import BaseModel

from src.user.schemas import UserShortAuthorSchemas


class MusicBaseSchemas(BaseModel):
    """Стандартная схема музыки"""
    title: str


class MusicCreateSchemas(BaseModel):
    """Схема создания музыки"""
    owner_id: int
    authors: list


class MusicResponseSchemasNoFile(BaseModel):
    id: int
    owner: UserShortAuthorSchemas


class MusicResponseSchemas(MusicBaseSchemas):
    """Информация о музыке"""
    id: int
    owner: UserShortAuthorSchemas
    authors: list
    file_url: str
    duration: float

