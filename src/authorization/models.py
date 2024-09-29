from sqlalchemy import Column, String, DateTime

from src.settings.models import BaseModel


class TokenModel(BaseModel):
    """Модель jwt токенов"""
    __tablename__ = "token"
    token = Column(String, nullable=False, unique=False)
    expire = Column(DateTime, nullable=False)
