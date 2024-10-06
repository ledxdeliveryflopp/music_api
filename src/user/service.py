from dataclasses import dataclass

from fastapi import HTTPException, Depends, File
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.settings.database import get_session
from src.settings.exceptions import UserDontExist
from src.user.models import UserModel
from src.user.repository import UserRepository


@dataclass
class UserService(UserRepository):
    """Сервис пользователей"""

    async def _service_find_user_by_email(self, email: str) -> UserModel | None:
        """Поиск пользователя по email"""
        user = await self._repository_find_user_by_email(email)
        return user

    async def service_find_users_by_username(self, username: str) -> UserModel | HTTPException:
        """Поиск пользователя по email"""
        user = await self._repository_find_users_by_username(username)
        if not user:
            raise UserDontExist
        return user

    async def service_upload(self, request: Request, avatar:  File()):
        return await self.add_image(request, avatar)


async def init_user_service(session: AsyncSession = Depends(get_session)):
    """Инициализация сервиса пользователей"""
    return UserService(session=session)
