from fastapi import FastAPI
from app.api import all_routers
from app.config import settings
from fastapi_pagination import add_pagination
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend())
    yield


app = FastAPI(title="Stakewolle Task", lifespan=lifespan)
add_pagination(app) #Для автогенерации пагинации


for router in all_routers:
    app.include_router(router, prefix=settings.api_prefix)

