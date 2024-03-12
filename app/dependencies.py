from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.security.token_handler import TokenHandler
from app.schemas import users as user_schema
from app import models
from jose import JWTError
from app.database.uow import UOW_DEP
from app.utils.exceptions import IncorrectTokenFormatException, UserIsNotPresentException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(uow: UOW_DEP, token: Annotated[str, Depends(oauth2_scheme)]) -> models.User:
    
    try:
        payload = TokenHandler.decode(token)
        
    except JWTError:
        raise IncorrectTokenFormatException
    
    email: str = payload.get("sub")
    if email is None:
        raise UserIsNotPresentException
    token_data = user_schema.TokenData(email=email)
    
    async with uow:
        user = await uow.users.get_one_or_none(email=token_data.email)
        
        if user is None:
            raise UserIsNotPresentException
        return user


CURRENT_USER_DEP = Annotated[models.User, Depends(get_current_user)]