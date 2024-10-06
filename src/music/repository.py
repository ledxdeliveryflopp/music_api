import base64
import os
from dataclasses import dataclass

import aiofiles
from fastapi import File
from loguru import logger
from mutagen.mp3 import MP3
from sqlalchemy import Select, or_
from starlette.requests import Request

from src.music.models import MusicModel
from src.music.schemas import MusicCreateSchemas
from src.settings.exceptions import MusicSaveError, MusicDontExist, UserDontExist
from src.settings.models import BaseModel
from src.settings.service import BaseService
from src.user.models import UserModel


@dataclass
class MusicRepository(BaseService):
    """Репозиторий для работы с музыкой"""

    async def __find_user(self, id: int) -> UserModel:
        """Поиск пользователя по id"""
        user = await self.session.execute(Select(UserModel).where(UserModel.id == id))
        return user.scalar()

    async def _repository_find_music_by_id(self, id: int) -> MusicModel:
        """Поиск музыки по id"""
        music = await self.session.execute(Select(MusicModel).where(MusicModel.id == id))
        return music.scalar()

    async def _repository_find_music_by_author_or_title(self, author_username: str,
                                                        music_title: str) -> MusicModel:
        """Поиск музыки по username автора или названию песни"""
        music = await self.session.execute(Select(MusicModel).join(UserModel.musics).where(or_(
            UserModel.username == author_username, MusicModel.title == music_title)))
        return music.scalars().all()

    async def _repository_upload_music(self, schemas: MusicCreateSchemas) -> MusicModel:
        """Загрузка музыки"""
        user = await self.__find_user(schemas.owner_id)
        if not user:
            raise UserDontExist
        authors_list: list = [user.username]
        for i in schemas.authors:
            authors_list.append(i)
        new_music = MusicModel(owner_id=schemas.owner_id,  authors=authors_list)
        await self.service_save_object(new_music)
        return new_music

    @staticmethod
    async def _repository_get_music_duration(file_path: str) -> float:
        duration = MP3(file_path).info.length
        return duration

    async def _repository_upload_music_cover(self, music_id: int, request: Request,
                                             cover_file: File()) -> dict:
        """Загрузка обложки музыки"""
        music = await self._repository_find_music_by_id(music_id)
        if not music:
            raise MusicDontExist
        try:
            filename = cover_file.filename.replace(" ", "-")
            async with aiofiles.open(f"static/music/cover/{filename}", "wb+") as file:
                cover_data = await cover_file.read()
                await file.write(cover_data)
            cover_url = request.url_for("static", path=f"music/cover/{filename}")
            cover_url = str(cover_url)
            music.cover_url = cover_url
            await self.service_save_object(music)
            return music
        except Exception as exc:
            path = os.path.exists(f"static/music/cover/{cover_file.filename}")
            if path is True:
                os.remove(f"static/music/cover/{cover_file.filename}")
                logger.error(f"upload music error - {exc}")
                raise MusicSaveError
            logger.error(f"upload music error - {exc}")
            raise MusicSaveError

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

    async def _repository_add_music_in_user_favorite(self, user_id: int, music_id: int) -> ...:
        """Добавить/убрать музыку в/из избранное пользователя"""
        user = await self.__find_user(user_id)
        if not user:
            raise UserDontExist
        music = await self._repository_find_music_by_id(music_id)
        if not music:
            raise MusicDontExist
        new_list = [music_id]
        user_fav = user.favorite_playlist
        if not user_fav:
            user.favorite_playlist = new_list
        else:
            for i in user.favorite_playlist:
                if i in new_list:
                    new_list.remove(i)
                else:
                    new_list.append(i)
        user.favorite_playlist = new_list
        await self.service_save_object(user)
        return {"detail": "success"}
