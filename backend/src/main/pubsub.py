from socketio.asgi import ASGIApp
from socketio.async_server import AsyncServer
from fastapi import FastAPI


def setup_socketio(api_prefix: str, fastapi: FastAPI) -> AsyncServer:
    server = AsyncServer(
        cors_allowed_origins="*",
        cors_credentials=True,
        engineio_logger=False,
    )

    app = ASGIApp(server)

    fastapi.mount(api_prefix, app, name="Socket IO")
    return server
