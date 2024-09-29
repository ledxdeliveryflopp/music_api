from fastapi import APIRouter, Depends

from src.registration.service import RegistrationService, init_registration_service
from src.registration.schemas import UserBaseSchemas, UserCreateSchemas

registration_router = APIRouter(prefix="/registration", tags=["auth"])


@registration_router.post("/", response_model=UserBaseSchemas)
async def router_create_user(schemas: UserCreateSchemas,
                             service: RegistrationService = Depends(init_registration_service)):
    return await service.service_create_user(schemas)
