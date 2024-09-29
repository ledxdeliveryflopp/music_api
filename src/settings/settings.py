from functools import lru_cache

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Настройки бд"""
    user: str
    password: str
    host: str
    port: str
    name: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def get_full_db_address(self) -> str:
        """Полный адрес БД"""
        return (f"postgresql+asyncpg://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.name}")


class JwtTokenSettings(BaseSettings):
    """Настройки jwt токена"""
    jwt_secret: str
    jwt_algorithm: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class APISettings(BaseSettings):

    api_host: str
    api_port: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class AllSettings(BaseSettings):
    database_settings: DatabaseSettings
    jwt_settings: JwtTokenSettings
    api_settings: APISettings


@lru_cache()
def init_settings():
    """Инициализация настроек"""
    all_settings = AllSettings(database_settings=DatabaseSettings(),
                               jwt_settings=JwtTokenSettings(), api_settings=APISettings())
    return all_settings


logger.info("settings inited")
settings = init_settings()
