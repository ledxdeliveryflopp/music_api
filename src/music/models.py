from sqlalchemy import Column, String, Integer, ForeignKey, ARRAY, Float
from sqlalchemy.orm import relationship

from src.settings.models import BaseModel


class MusicModel(BaseModel):
    """Модель трека"""
    __tablename__ = "music"
    title = Column(String, nullable=True, unique=False)
    file_url = Column(String, nullable=True, unique=True)
    cover_url = Column(String, nullable=True, unique=True)
    file_static_path = Column(String, nullable=True, unique=True)
    duration = Column(Float, nullable=True, unique=False)
    authors = Column(ARRAY(String), nullable=False, unique=False)
    play_numbers = Column(Integer(), default=0, nullable=True, unique=False)
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False,
                      unique=False)

    owner = relationship("UserModel", lazy="selectin", back_populates="musics",
                         foreign_keys=[owner_id])
