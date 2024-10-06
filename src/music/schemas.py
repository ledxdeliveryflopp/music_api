from pydantic import BaseModel


class MusicBaseSchemas(BaseModel):
    """Стандартная схема музыки"""
    title: str


class MusicCreateSchemas(BaseModel):
    """Схема создания музыки"""
    owner_id: int
    authors: list


class UserShortAuthorSchemas(BaseModel):
    """Модель минимальной информации о авторе"""
    username: str


class MusicResponseSchemasNoFile(BaseModel):
    id: int
    owner: UserShortAuthorSchemas


class MusicResponseSchemas(MusicBaseSchemas):
    """Информация о музыке"""
    id: int
    owner: UserShortAuthorSchemas
    authors: list
    cover_url: str
    file_url: str
    duration: float

