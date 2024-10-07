from dataclasses import dataclass

from fastapi import HTTPException
from sqlalchemy import Select

from src.authorization.models import TokenModel
from src.authorization.schemas import LoginSchemas
from src.authorization.utils import create_token
from src.settings.exceptions import UserDontExist
from src.settings.service import BaseService
from src.user.models import UserModel


@dataclass
class AuthorizationRepository(BaseService):
    """Репозиторий jwt токенов"""

    async def _repository_find_user_by_email(self, email: str) -> UserModel | None:
        """Поиск пользователя по email"""
        user = await self.session.execute(Select(UserModel).where(UserModel.email == email))
        return user.scalar()

    async def __repository_create_access_token(self, email: str) -> dict:
        """Сохранение токена"""
        user = await self._repository_find_user_by_email(email)
        if not user:
            raise UserDontExist
        user_id = user.id
        token_data = await create_token(email, user_id)
        token = TokenModel(token=token_data.get("token"), expire=token_data.get("expire"))
        await self.service_save_object(token)
        return token_data

    async def _repository_login(self, schemas: LoginSchemas) -> dict | HTTPException:
        """Авторизация"""
        return await self.__repository_create_access_token(schemas.email)
