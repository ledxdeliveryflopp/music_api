import random
import string
from datetime import datetime, timedelta

from jose import jwt
from loguru import logger
from passlib.context import CryptContext

from src.settings.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@logger.catch
async def create_token(email: str, user_id: int) -> dict:
    """Создание токена"""
    expire_data = datetime.utcnow() + timedelta(minutes=15)
    random_string: str = random.choices(string.printable, k=random.randint(5, 15))
    token_payload: dict = {"user_email": email, "user_id": user_id, "random_str": random_string}
    jwt_token = jwt.encode(token_payload, settings.jwt_settings.jwt_secret,
                           settings.jwt_settings.jwt_algorithm)
    return {"token": jwt_token, "expire": expire_data}


@logger.catch
async def decode_token_data(jwt_token: str) -> dict:
    """Дешифровка токена"""
    payload_data = jwt.decode(jwt_token, settings.jwt_settings.jwt_secret,
                              settings.jwt_settings.jwt_algorithm)
    user_id = payload_data.get("user_id")
    return {"user_id": user_id}


@logger.catch
async def verify_password(plain_password: str, password: str):
    """Проверка пароля"""
    return pwd_context.verify(plain_password, password)
