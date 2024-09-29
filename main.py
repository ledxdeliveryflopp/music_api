from loguru import logger
import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.authorization.router import authorization_router
from src.registration.router import registration_router
from src.user.router import user_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router)
app.include_router(registration_router)
app.include_router(authorization_router)


@logger.catch
def run_app(host: str, port: int) -> None:
    """Запуск приложения"""
    uvicorn.run(app=app, host=host, port=port, log_config="log.ini")


if __name__ == "__main__":
    logger.add("application.log", rotation="100 MB",
               format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")
    logger.info("application started")
    run_app("127.0.0.1", 7000)
