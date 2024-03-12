from app.models import Base
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column
from datetime import datetime
    
class ReferralCode(Base):
    __tablename__ = 'referral_codes'
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    code: Mapped[str] = mapped_column(unique=True)
    expiration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(server_default="True")