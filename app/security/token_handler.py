from datetime import datetime, timedelta
from jose import  jwt
from app.config import settings



class TokenHandler:
    
    @classmethod
    def encode(cls, payload: dict) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload.update({"exp": expire})
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @classmethod
    def decode(cls, token: str) -> dict:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        encoded_jwt = cls.encode(data)
        return encoded_jwt
    
