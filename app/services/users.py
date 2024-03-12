from app.schemas import users as user_schema
from app.security.password_handler import PasswordHandler
from app.security.token_handler import TokenHandler
from app.database.uow import UnitOfWork
from app import models
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.exceptions import (
    IncorrectEmailOrPasswordException,
    UserAlreadyExistsException,
)


class UsersService:

    async def login_user(
        self,
        uow: UnitOfWork,
        user_data: OAuth2PasswordRequestForm,
    ) -> user_schema.TokenSchema:
        """
        Authentication
        Используем OAuth2 Form-data -> где поле username = user.email
        """
        async with uow:
            user: models.User = await uow.users.get_one_or_none(
                email=user_data.username
            )
            if not user or not PasswordHandler.verify(
                user_data.password, user.password
            ):
                raise IncorrectEmailOrPasswordException

            access_token = TokenHandler.create_access_token(data={"sub": user.email})
            return user_schema.TokenSchema(access_token=access_token)

    # Register
    async def create_user(
        self,
        uow: UnitOfWork,
        user_data: user_schema.CreateUserSchema,
        referral_code: str | None,
    ) -> models.User:

        async with uow:

            existing_user = await uow.users.get_one_or_none(email=user_data.email)
            if existing_user:
                raise UserAlreadyExistsException

            hashed_password = PasswordHandler.hash(user_data.password)
            user_data.password = hashed_password
            user_dict = user_data.model_dump()

            if referral_code:
                """
                Зависимостью мы уже проверил expired or not, теперь мы просто проверим передан или нет,
                если нет, то зачем делать запрос в бд и тратить лишнее время.
                Если передан, то мы в dict добавляем referrer_user_id = user.id которому принадлежит реф. код
                """
                existing_ref_code: models.ReferralCode = (
                    await uow.referral_codes.get_one_or_none(code=referral_code)
                )
                user_dict["referrer_user_id"] = existing_ref_code.user_id

            user = await uow.users.create(data=user_dict)
            await uow.commit()
            return user


users_service = UsersService()
