from dataclasses import dataclass

from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.authorization.repository import AuthorizationRepository
from src.authorization.schemas import LoginSchemas
from src.authorization.utils import verify_password
from src.settings.database import get_session
from src.settings.exceptions import UserDontExist, BadCredentials, TokenException


@dataclass
class AuthorizationService(AuthorizationRepository):
    """Сервис авторизации"""

    async def service_check_token(self, token: str) -> dict | HTTPException:
        """Проверка токена"""
        jwt_token = await self._repository_find_token(token)
        if not jwt_token:
            raise TokenException
        return {"detail": True}

    async def service_login(self, schemas: LoginSchemas) -> dict | HTTPException:
        """Авторизация"""
        user = await self._repository_find_user_by_email(schemas.email)
        if not user:
            raise UserDontExist
        verify = await verify_password(schemas.password, user.password)
        if not verify:
            raise BadCredentials
        return await self._repository_login(schemas)


async def init_authorization_service(session: AsyncSession = Depends(get_session)):
    """Инициализая сервиса авторизации"""
    return AuthorizationService(session)
