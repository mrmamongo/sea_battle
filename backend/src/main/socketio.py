import socketio
import json

from socketio import AsyncNamespace
from fastapi import FastAPI
from sanic import Sanic
from sanic.response import text
from src.presentation.socketio.namespace import GameNamespace


def setup_socketio(api_prefix: str, fastapi: FastAPI) -> AsyncServer:
    server = socketio.AsyncServer(cors_allowed_origins="*", cors_credentials=True, engineio_logger=False, )
    server.register_namespace(GameNamespace('/game'))

    app = socketio.ASGIApp(server)

    fastapi.mount(api_prefix, app, name="Socket IO")
    return server
