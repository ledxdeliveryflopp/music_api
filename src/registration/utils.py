from loguru import logger
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@logger.catch
def hash_password(password: str):
    """Хэширование пароля"""
    return pwd_context.hash(password)
