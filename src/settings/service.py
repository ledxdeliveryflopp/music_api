from dataclasses import dataclass

from src.settings.models import BaseModel
from src.settings.repository import BaseRepository


@dataclass
class BaseService(BaseRepository):
    """Сервис работы с БД"""

    async def service_save_object(self, saved_object: BaseModel) -> BaseModel:
        """Сохранение объекта в БД"""
        return await self._repository_save_object(saved_object)

    async def service_delete_object(self, deleted_object: BaseModel) -> BaseModel:
        """Удаление объекта из БД"""
        return await self._repository_delete_object(deleted_object)
