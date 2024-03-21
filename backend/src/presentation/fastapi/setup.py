from fastapi import FastAPI
from starlette import status

from src.presentation.fastapi.exception_handlers import setup_exception_handlers
from src.presentation.fastapi.routes.bot import handle_update
from src.presentation.fastapi.routes.auth import router as auth_router
from src.presentation.fastapi.routes.game import router as game_router


def setup_routes(app: FastAPI, token: str) -> None:
    app.post(f"/api/{token}", status_code=status.HTTP_200_OK, include_in_schema=False)(
        handle_update
    )
    app.include_router(auth_router, prefix="/api")
    app.include_router(game_router, prefix="/api")
    setup_exception_handlers(app)
