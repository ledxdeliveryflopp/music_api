from fastapi import APIRouter
from starlette.requests import Request

static_router = APIRouter(prefix="/app", tags=['static for app'])


@static_router.get('/tray_icon/')
async def static_tray_icon_router(request: Request):
    """Роутер для получение иконки треи приложениия для восстановления"""
    icon_url = request.url_for("static", path=f"app/tray_icon.png")
    icon_url = str(icon_url)
    return {"icon": icon_url}
