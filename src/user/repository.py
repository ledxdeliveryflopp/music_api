from dataclasses import dataclass

import aiofiles
from fastapi import HTTPException, File
from loguru import logger
from sqlalchemy import Select
from starlette.requests import Request

from src.settings.exceptions import UserDontExist
from src.settings.service import BaseService
from src.user.models import UserModel


@dataclass
class UserRepository(BaseService):
    """Репозиторий пользователей"""

    async def _repository_find_user_by_email(self, email: str) -> UserModel | None:
        """Поиск пользователя по email"""
        user = await self.session.execute(Select(UserModel).where(UserModel.email == email))
        return user.scalar()

    async def _repository_find_users_by_username(self, username: str) -> UserModel | HTTPException:
        """Поиск пользователя по email"""
        user = await self.session.execute(Select(UserModel).where(UserModel.username == username))
        if not user:
            raise UserDontExist
        return user.scalars().all()

    @staticmethod
    async def add_image(request: Request, avatar:  File()):
        async with aiofiles.open(f"static/avatars/{avatar.filename}", "wb+") as file:
            avatar_data = await avatar.read()
            await file.write(avatar_data)
            avatar_url = request.url_for("static", path=f"avatars/{avatar.filename}")
            logger.debug(f"avatar url - {avatar_url}")
        return avatar_url
