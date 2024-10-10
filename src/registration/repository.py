from dataclasses import dataclass

from sqlalchemy import Select

from src.registration.schemas import UserCreateSchemas
from src.registration.utils import hash_password
from src.settings.service import BaseService
from src.user.models import UserModel



@dataclass
class RegistrationRepository(BaseService):
    """Репозиторий регистрации"""

    async def _repository_find_user_by_email(self, email: str) -> UserModel | None:
        """Поиск пользователя по email"""
        user = await self.session.execute(Select(UserModel).where(UserModel.email == email))
        return user.scalar()

    async def _repository_create_user(self, schemas: UserCreateSchemas) -> UserModel:
        """Создание пользователя"""
        new_user = UserModel(**schemas.dict(exclude="password"), password=hash_password(
            schemas.password))
        await self._repository_save_object(new_user)
        return new_user
