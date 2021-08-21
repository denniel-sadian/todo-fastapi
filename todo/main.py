from fastapi import FastAPI

from .users.routes import router as users_router
from .items.routes import router as items_router
from .config import settings
from .db import database

app = FastAPI(title=settings.APP_NAME)


@app.on_event('startup')
async def startup() -> None:
    if not database.is_connected:
        await database.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    if database.is_connected:
        await database.disconnect()


app.include_router(users_router)
app.include_router(items_router)
