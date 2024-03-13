from fastapi import APIRouter, Depends
from app.services.users import users_service
from app.database.uow import UOW_DEP
from app.schemas import users as user_schema
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.dependencies import CURRENT_USER_DEP
from app.permissions import Permissions

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post('/register', dependencies=[Depends(Permissions.is_referral_code_given_and_unexpired), Depends(Permissions.has_verified_email)])
async def create_user(
    uow: UOW_DEP,
    user_data: user_schema.CreateUserSchema,
    referral_code: str | None = None,
) -> user_schema.UserSchema:
    """
    - Если передать referral_code -> возможность регистрации по реферальному коду в качестве реферала;
    """
    return await users_service.create_user(
        uow=uow,
        user_data=user_data,
        referral_code=referral_code
    )

@router.post('/login')
async def login_user(
    uow: UOW_DEP,
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> user_schema.TokenSchema:
    return await users_service.login_user(
        uow=uow,
        user_data=user_data
    )


@router.get('/me')
async def read_me(
    current_user: CURRENT_USER_DEP
) -> user_schema.UserSchema:
    return current_user