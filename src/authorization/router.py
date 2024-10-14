from fastapi import APIRouter, Depends, HTTPException

from src.authorization.schemas import LoginSchemas, TokenSchemas
from src.authorization.service import AuthorizationService, init_authorization_service

authorization_router = APIRouter(prefix="/authorization", tags=["auth"])


@authorization_router.post("/check_token/", response_model=None)
async def router_check_token(token: str,
                             service: AuthorizationService = Depends(init_authorization_service)) -> dict | HTTPException:
    """Роутер проверки токена"""
    return await service.service_check_token(token)


@authorization_router.post("/login/", response_model=TokenSchemas)
async def router_login(schemas: LoginSchemas,
                       service: AuthorizationService = Depends(init_authorization_service)) -> dict | HTTPException:
    """Роутер логина"""
    return await service.service_login(schemas)
