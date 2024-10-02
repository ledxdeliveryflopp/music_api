from fastapi import APIRouter, Depends, File, UploadFile
from starlette.requests import Request
from starlette.responses import StreamingResponse

from src.music.schemas import MusicResponseSchemas, MusicCreateSchemas, MusicResponseSchemasNoFile
from src.music.service import MusicService, init_music_service

music_router = APIRouter(prefix="/music", tags=["music"])


@music_router.post("/upload/", response_model=MusicResponseSchemasNoFile)
async def router_upload_music(schemas: MusicCreateSchemas,
                              service: MusicService = Depends(init_music_service)) -> dict:
    """Роутер зарузки музыки"""
    return await service.service_upload_music(schemas)


@music_router.patch("/upload_music_file/", response_model=MusicResponseSchemas)
async def router_upload_music_file(music_id: int, request: Request,
                                   music_file: UploadFile = File(),
                                   service: MusicService = Depends(init_music_service)) -> dict:
    """Роутер загрузки mp3 файла"""
    return await service.service_upload_music_file(music_id, request, music_file)


@music_router.get("/find_music/", response_model=MusicResponseSchemas)
async def router_find_music_by_id(music_id: int,
                                  service: MusicService = Depends(init_music_service)):
    """Роутер поиска музыки по id"""
    return await service.service_find_music_by_id(music_id)


@music_router.get("/play_music/")
async def router_stream_music(music_id: int, service: MusicService = Depends(init_music_service)):
    """Роутер стриминга музыки"""
    return StreamingResponse(service.service_stream_music(music_id), media_type="audio/mp3")

