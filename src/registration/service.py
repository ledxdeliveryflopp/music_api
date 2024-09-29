from dataclasses import dataclass

from fastapi import HTTPException, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.registration.repository import RegistrationRepository
from src.settings.database import get_session
from src.settings.exceptions import UserAlreadyExist
from src.user.models import UserModel
from src.user.schemas import UserCreateSchemas


@dataclass
class RegistrationService(RegistrationRepository):
    """Репозиторий регистрации"""

    async def service_create_user(self, schemas: UserCreateSchemas) -> UserModel | HTTPException:
        """Создание пользователя"""
        user = await self._repository_find_user_by_email(schemas.email)
        if user:
            logger.error(f"{self.service_create_user.__name__} - user {schemas.email} already "
                         f"exist")
            raise UserAlreadyExist
        new_user = await self._repository_create_user(schemas)
        return new_user


async def init_registration_service(session: AsyncSession = Depends(get_session)):
    """Инициализация сервиса регистрации"""
    return RegistrationService(session)
