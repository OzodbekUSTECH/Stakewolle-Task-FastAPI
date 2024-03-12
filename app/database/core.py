from app.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


engine = create_async_engine(settings.DATABASE_URL, echo=settings.ECHO)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)