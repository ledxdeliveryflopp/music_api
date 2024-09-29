from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from src.settings.settings import settings

async_engine = create_async_engine(url=settings.database_settings.get_full_db_address, echo=False)

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_session():
    """Генерация сессии к бд"""
    async with async_session() as session:
        yield session
