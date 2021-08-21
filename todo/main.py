from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


app.include_router(users_router)
app.include_router(items_router)
