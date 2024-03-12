from app.models import Base
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import ReferralCode
    
class User(Base):
    __tablename__ = 'users'
    
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    
    referrer_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id")) # Ссылка на пользователя, который дал рефералку
 
    referral_codes: Mapped[list["ReferralCode"]] = relationship(lazy="subquery") #Это реф коды юзера

