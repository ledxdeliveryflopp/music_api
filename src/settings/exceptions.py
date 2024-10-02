from typing import Any
from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail, **kwargs)


class UserAlreadyExist(DetailedHTTPException):
    """Пользователь уже существует"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Пользователь с таким email существует."


class UserDontExist(DetailedHTTPException):
    """Пользователя не существует"""
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователя не существует."


class MusicSaveError(DetailedHTTPException):
    """Ошибка при сохранении музыки"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Ошибка при сохранении музыки."


class MusicDontExist(DetailedHTTPException):
    """Музыки ге существует"""
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Такого трека не существует."


class BadCredentials(DetailedHTTPException):
    """Не верная почта или пароль"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Не верная почта или пароль."


class DatabaseSaveError(DetailedHTTPException):
    """Исключение при сохранении в БД"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Ошибка сохранения."


class DatabaseDeleteError(DetailedHTTPException):
    """Исключение при удалении из БД"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Ошибка удаления."
