import socketio
import json


from typing import Annotated
from functools import lru_cache
from fastapi import FastAPI
from sanic import Sanic
from sanic.response import text


def setup_socketio(api_prefix: str, fastapi: FastAPI) -> AsyncServer:
    server = socketio.AsyncServer(cors_allowed_origins="*", cors_credentials=True, engineio_logger=False, )
    server.register_namespace(MyCustomNamespace('/game'))

    app = socketio.ASGIApp(server)

    fastapi.mount(api_prefix, app, name="Socket IO")
    return server
