from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete
from fastapi_pagination.ext.sqlalchemy import paginate

class BaseRepository:
    def __init__(self, session: AsyncSession, model: DeclarativeMeta):
        self.session = session
        self.model = model

    async def bulk_create(self, data_list: list[dict]):
        stmt = insert(self.model).values(data_list).returning(self.model)
        await self.session.execute(stmt)

    async def create(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_all(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        return await paginate(self.session, stmt)

    async def get_by_id(self, id: int) -> dict:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_one_or_none(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, id: int, data: dict) -> dict:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete(self, id: int) -> dict:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()
        


    
    
    


