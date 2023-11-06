from fastapi import status, HTTPException


class UserAlreadyExistsException(HTTPException):
    status_code = status.HTTP_409_CONFLICT,
    detail = 'Пользователь уже зарегистрирован'


class IncorrectEmailOrPasswordException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = 'Неверная почта или пароль'


class TokenExpiredException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = 'Токен истек'


class TokenAbsentException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = 'Токен отсутствует'


class IncorrectTokenFormatException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = 'Некорректный формат токена'


class UserIsNotPresentException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED,






