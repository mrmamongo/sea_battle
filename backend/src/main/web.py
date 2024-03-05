from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import ApiConfig
from src.presentation.fastapi.setup import setup_routes


def setup_fastapi(config: ApiConfig, token: str) -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=config.allow_credentials,
        allow_methods=config.allow_methods,
        allow_headers=config.allow_headers,
    )
    
    setup_routes(app, token)

    return app

