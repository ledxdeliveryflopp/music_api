from dataclasses import dataclass

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.settings.exceptions import DatabaseDeleteError, DatabaseSaveError
from src.settings.models import BaseModel


@dataclass
class BaseRepository:
    """Репозиторий работы с БД"""
    session: AsyncSession

    async def _repository_save_object(self, saved_object: BaseModel) -> None:
        """Сохранение объекта в БД"""
        try:
            self.session.add(saved_object)
            await self.session.commit()
            await self.session.refresh(saved_object)
        except Exception as exc:
            await self.session.rollback()
            logger.error(f"database save exception - {exc}")
            raise DatabaseSaveError

    async def _repository_delete_object(self, deleted_object: BaseModel) -> None:
        """Удаление объекта из БД"""
        try:
            await self.session.delete(deleted_object)
            await self.session.commit()
        except Exception as exc:
            await self.session.rollback()
            logger.error(f"database delete exception - {exc}")
            raise DatabaseDeleteError
