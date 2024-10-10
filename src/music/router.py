from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.security import HTTPBearer
from starlette.requests import Request
from starlette.responses import StreamingResponse

from src.music.schemas import MusicResponseSchemas, MusicCreateSchemas, MusicResponseSchemasNoFile
from src.music.service import MusicService, init_music_service

music_router = APIRouter(prefix="/music", tags=["music"])

token_protection = HTTPBearer()


@music_router.post("/upload/", response_model=MusicResponseSchemasNoFile)
async def router_upload_music(schemas: MusicCreateSchemas, request: Request,
                              token: str = Depends(token_protection),
                              service: MusicService = Depends(init_music_service)) -> dict:
    """Роутер зарузки музыки"""
    return await service.service_upload_music(request, schemas)


@music_router.patch("/upload_music_file/")
async def router_upload_music_file(music_id: int, request: Request,
                                   music_file: UploadFile = File(),
                                   service: MusicService = Depends(init_music_service)) -> dict:
    """Роутер загрузки mp3 файла"""
    return await service.service_upload_music_file(music_id, request, music_file)


@music_router.patch("/upload_cover_file/")
async def router_upload_cover_file(music_id: int, request: Request,
                                   cover_file: UploadFile = File(),
                                   service: MusicService = Depends(init_music_service)) -> dict:
    """Роутер загрузки файла обложки"""
    return await service.service_upload_music_cover(music_id, request, cover_file)


@music_router.get("/find_music_id/", response_model=MusicResponseSchemas)
async def router_find_music_by_id(music_id: int,
                                  service: MusicService = Depends(init_music_service)):
    """Роутер поиска музыки по id"""
    return await service.service_find_music_by_id(music_id)


@music_router.get("/music_by_play_count/", response_model=list[MusicResponseSchemas])
async def router_sort_music_by_play_count(service: MusicService = Depends(init_music_service)):
    """Роутер сортировки музыки по колличеству прослушиваний"""
    return await service.service_sort_music_by_play_count()


@music_router.get("/find_music/", response_model=list[MusicResponseSchemas])
async def router_find_music_by_author_or_title(author_username: str | None = None,
                                               music_title: str | None = None,
                                               service: MusicService = Depends(init_music_service)):
    """Роутер поиска музыки по автору или названию"""
    return await service.service_find_music_by_author_or_title(author_username, music_title)


@music_router.get("/play_music/", response_model=MusicResponseSchemas)
async def router_play_music_by_id(music_id: int, request: Request,
                                  token: str = Depends(token_protection),
                                  service: MusicService = Depends(init_music_service)):
    """Роутер проигрывания музыки по id"""
    return await service.service_play_music_by_id(request, music_id)


@music_router.get("/stream_music/")
async def router_stream_music(music_id: int, service: MusicService = Depends(init_music_service)):
    """Роутер стриминга музыки"""
    return StreamingResponse(service.service_stream_music(music_id), media_type="audio/mp3")


@music_router.patch("/add_to_fav/")
async def router_add_music_in_user_favorite(user_id: int, music_id: int,
                                            service: MusicService = Depends(init_music_service)):
    """Роутер стриминга музыки"""
    return await service.service_add_music_in_user_favorite(user_id, music_id)

