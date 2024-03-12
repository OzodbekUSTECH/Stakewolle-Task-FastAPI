from passlib.context import CryptContext
from app.config import settings


class PasswordHandler:
    pwd_context = CryptContext(
        schemes=[settings.HASHING_SCHEME],
        deprecated="auto",
    )

    @staticmethod
    def hash(password: str):
        return PasswordHandler.pwd_context.hash(password)

    @staticmethod
    def verify(plain_password, hashed_password):
        return PasswordHandler.pwd_context.verify(plain_password, hashed_password)
    