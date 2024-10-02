import base64
import os
from dataclasses import dataclass

import aiofiles
from fastapi import File
from loguru import logger
from mutagen.mp3 import MP3
from sqlalchemy import Select
from starlette.requests import Request

from src.music.models import MusicModel
from src.music.schemas import MusicCreateSchemas
from src.settings.exceptions import MusicSaveError, MusicDontExist
from src.settings.service import BaseService
from src.user.models import UserModel


@dataclass
class MusicRepository(BaseService):
    """Репозиторий для работы с музыкой"""

    @logger.catch
    async def __find_user(self, id: int) -> UserModel:
        """Поиск пользователя по id"""
        user = await self.session.execute(Select(UserModel).where(UserModel.id == id))
        return user.scalar()

    @logger.catch
    async def _repository_find_music_by_id(self, id: int) -> MusicModel:
        """Поиск музыки по id"""
        music = await self.session.execute(Select(MusicModel).where(MusicModel.id == id))
        return music.scalar()

    @logger.catch
    async def _repository_upload_music(self, schemas: MusicCreateSchemas) -> MusicModel:
        """Загрузка музыки"""
        author = await self.__find_user(schemas.owner_id)
        authors_list: list = [author.username]
        for i in schemas.authors:
            authors_list.append(i)
        new_music = MusicModel(owner_id=schemas.owner_id,  authors=authors_list)
        await self.service_save_object(new_music)
        return new_music

    @logger.catch
    async def _repository_get_music_duration(self, file_path: str) -> float:
        duration = MP3(file_path).info.length
        return duration

    @logger.catch
    async def _repository_upload_music_file(self, music_id: int, request: Request,
                                            music_file: File()) -> dict:
        """Загрузка файла музыки"""
        music = await self._repository_find_music_by_id(music_id)
        if not music:
            raise MusicDontExist
        try:
            filename = music_file.filename.replace(" ", "-")
            async with (aiofiles.open(f"static/music/{filename}", "wb+") as file,
                        aiofiles.open(f"static/music/temp/{music_id}.mp3", "wb+") as decoded_file):
                music_data = await music_file.read()
                stored__data = music_data
                base64_encoded_data = base64.b64encode(music_data)
                await file.write(base64_encoded_data)
                await decoded_file.write(stored__data)
                duration = await self._repository_get_music_duration(f"static/music/temp/{music_id}.mp3")
            os.remove(f"static/music/temp/{music_id}.mp3")
            music_url = request.url_for("static", path=f"music/{filename}")
            music_url = str(music_url)
            title = music_file.filename.split(".mp3")
            music.title = title[0]
            music.file_url = music_url
            music.duration = duration
            music.file_static_path = f"static/music/{music_file.filename}"
            await self.service_save_object(music)

            return music
        except Exception as exc:
            path = os.path.exists(f"static/music/{music_file.filename}")
            if path is True:
                os.remove(f"static/music/{music_file.filename}")
                logger.error(f"upload music error - {exc}")
                raise MusicSaveError
            logger.error(f"upload music error - {exc}")
            raise MusicSaveError

