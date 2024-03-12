from app.schemas import BaseSchema
from pydantic import EmailStr, BaseModel, Field

class TokenSchema(BaseModel):
    access_token: str

class TokenData(BaseModel):
    email: EmailStr


class CreateUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str



class UserSchema(BaseSchema, CreateUserSchema):
    password: str = Field(exclude=True) #Убираем вывод пароля в запросе!
    referrer_user_id: int | None