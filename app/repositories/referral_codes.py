from app.repositories import BaseRepository
from sqlalchemy import select, func
from datetime import datetime

class ReferralCodesRepository(BaseRepository):
    
    async def get_one_active_ref_code_or_none_of_user(self, user_id: int):
        current_datetime = datetime.utcnow()  # Текущая дата и время
        stmt = select(self.model).filter(
            self.model.user_id == user_id,
            self.model.is_active == True,
            self.model.expiration_date > current_datetime,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()