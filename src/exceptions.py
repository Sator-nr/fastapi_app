from fastapi import status, HTTPException


UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь уже зарегистрирован'
)


IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверная почта или пароль'
)


TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен истек'
)


TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен отсутствует'
)


IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Некорректный формат токена'
)


UserIsNotPresentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED
)

RoomCanNotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Не осталось свободных номеров'
)

NoBookingException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Не существует указанной брони для данного пользователя'
)




