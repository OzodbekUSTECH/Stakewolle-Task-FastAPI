from fastapi import HTTPException, status

class BaseException(HTTPException):
    status_code = 500 # <-- задаем значения по умолчанию
    detail = ""
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsException(BaseException): 
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"

class UserDoesNotExistException(BaseException):
    status_code=status.HTTP_404_NOT_FOUND
    status="Юзер не найден или не существует"

class IncorrectEmailOrPasswordException(BaseException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверная почта или пароль"

class IncorrectTokenFormatException(BaseException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"

class UserIsNotPresentException(BaseException):
    status_code=status.HTTP_401_UNAUTHORIZED

class UserDoesNotHaveReferralCodeException(BaseException):
    status_code=status.HTTP_404_NOT_FOUND
    status="У пользователя нет реферального кода"



class ReferralCodeAlreadyExistsException(BaseException):
    status_code=status.HTTP_403_FORBIDDEN
    detail="Реферальный код уже существует (только 1 код можно создать!)"

class ReferralCodeExpiredException(BaseException):
    status_code=status.HTTP_403_FORBIDDEN
    detail="Реферальный код истёк!"

class ReferralCodeDoesNotExistException(BaseException):
    status_code=status.HTTP_403_FORBIDDEN
    detail="Реферальный код не существует"



class NotAllowedToDeleteReferralCodeException(BaseException):
    status_code=status.HTTP_403_FORBIDDEN
    detail="ВЫ не можете удалить этот реферальный код!"

class NotAllowedMethodException(BaseException):
    status_code=status.HTTP_403_FORBIDDEN
    detail="Not allowed method!"