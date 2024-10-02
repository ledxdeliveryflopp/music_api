from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.settings.models import BaseModel


class UserModel(BaseModel):
    """Модель пользователя"""
    __tablename__ = "user"
    username = Column(String(length=16), unique=False, nullable=False)
    email = Column(String(length=255), unique=True, nullable=False)
    password = Column(String(length=255), unique=False, nullable=False)
    avatar_url = Column(String, unique=False, nullable=True,
                        default="http://localhost:7000/static/avatars/default.png")

    musics = relationship("MusicModel", lazy="selectin", back_populates="owner")