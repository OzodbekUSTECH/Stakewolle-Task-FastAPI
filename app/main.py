import uvicorn
from fastapi import FastAPI
from app.api import all_routers
from app.config import settings
from fastapi_pagination import add_pagination

app = FastAPI(title="Stakewolle Task")
add_pagination(app) #Для автогенерации пагинации


for router in all_routers:
    app.include_router(router, prefix=settings.api_prefix)

