from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.security import HTTPBearer
from starlette.requests import Request

from src.user.schemas import UserSchemas
from src.user.service import UserService, init_user_service

user_router = APIRouter(prefix="/user", tags=["users"])


token_protection = HTTPBearer()


@user_router.get("/find-user/", response_model=list[UserSchemas])
async def router_find_user_by_username(username: str, token: str = Depends(token_protection),
                                       service: UserService = Depends(init_user_service)):
    return await service.service_find_users_by_username(username)


@user_router.post("/upload/")
async def router_upload(request: Request, avatar: UploadFile = File(),
                        service: UserService = Depends(init_user_service)):
    return await service.service_upload(request, avatar)
