from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func, DateTime
from datetime import datetime

class Base(DeclarativeBase):
    __abstract__ = True 

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 
    
    
    