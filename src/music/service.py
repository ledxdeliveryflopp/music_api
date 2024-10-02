import base64
from dataclasses import dataclass

import aiofiles
from fastapi import File, Depends
from loguru import logger
from mutagen.mp3 import MP3
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.music.models import MusicModel
from src.music.repository import MusicRepository
from src.music.schemas import MusicCreateSchemas
from src.settings.database import get_session
from src.settings.exceptions import MusicDontExist


@dataclass
class MusicService(MusicRepository):
    """Сервис музыки"""

    async def service_upload_music(self, schemas: MusicCreateSchemas) -> MusicModel:
        """Загрузка музыки"""
        return await self._repository_upload_music(schemas)

    async def service_upload_music_file(self, music_id: int, request: Request,
                                        music_file: File()) -> MusicModel:
        """Загрузка музыки"""
        return await self._repository_upload_music_file(music_id, request, music_file)

    async def service_find_music_by_id(self, music_id: int):
        music = await self._repository_find_music_by_id(music_id)
        if not music:
            raise MusicDontExist
        return music

    async def service_stream_music(self, music_id: int):
        """Стриминг музыки"""
        music = await self._repository_find_music_by_id(music_id)
        music_static = music.file_static_path
        async with aiofiles.open(music_static, mode="rb") as file:
            data = await file.read()
            decoded_data = base64.b64decode(data)
            yield decoded_data


async def init_music_service(session: AsyncSession = Depends(get_session)) -> MusicService:
    """Инифиализация сервиса музыки"""
    return MusicService(session)
