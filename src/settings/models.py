from sqlalchemy import Column, Integer, func, DateTime

from src.settings.database import Base


class BaseModel(Base):
    """Абстрактная модель"""
    __abstract__ = True
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
