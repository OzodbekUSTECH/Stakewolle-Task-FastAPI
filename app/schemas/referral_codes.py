from app.schemas import BaseSchema
from pydantic import EmailStr, BaseModel, Field
from datetime import datetime

class CreateReferralCodeSchema(BaseModel):
    user_id: int
    code: str
    expiration_date: datetime


class ReferralCodeSchema(BaseSchema, CreateReferralCodeSchema):
    is_active: bool