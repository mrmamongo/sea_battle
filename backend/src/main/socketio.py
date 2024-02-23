import socketio
import uuid
import json
import redis
import redisjson as rj

from typing import Annotated
from functools import lru_cache
from fastapi import FastAPI
from socketio import AsyncServer, AsyncNamespace, async_mode
from sanic import Sanic
from sanic.response import text
from ../infra/postgres/gateways import SAGameSessionGateway
from ../redis/models import BoardDTO
from ../redis/game import BoardShooterDTO

from dishka.integrations.base import Depends
from dishka.integrations.fastapi import inject

# initialize a global Redis connection
r = redis.Redis()

class GameNamespace(AsyncNamespace):
    @lru_cache(maxsize=128)
    def get_game_state(self, game_id):
        # get the game state from Redis as a JSON object
        game_state = rj.get_json(game_id)
        return game_state
    
    @inject
    async def on_game_start(self, sid, data, game_session: Annotated[SAGameSessionGateway, Depends()]):
        first_player_games = await game_session.get_by_first_player(sid)
        if first_player_games == 0:
            #Generate uuid
            game_id = str(uuid.uuid4())
            await game_session.create(id=game_id, "Created", first_player=sid)
            #Joining room
            await self.join_room(game_id, sid)
            #Sending broadcast message about joining the game
            await self.send(sid, "You have joined the game.", room=game_id)
            # store the game state in Redis as a JSON object
            rj.create_json(game_id, {"state": data, "clients": [sid]})
        else:
            # get the game state from Redis as a JSON object
            game_state = self.get_game_state(sid)
            # update the game state with the user's data
            game_state["state"] = data
            # broadcast the updated game state to all clients in the game
            await self.send(room=game_id, json=game_state)

    @inject
    async def on_accept(self, sid, environ, room_id, game_session: Annotated[SAGameSessionGateway, Depends()]):
        # check if the user is already in a game room
        if await game_session.get_by_second_player(sid)
            # if so, send a message to the user to confirm they're already in a game
            await self.send(sid, "You are already in a game.", room=sid)
        #else join the room
        else:
            game_session.update(room_id, second_player=sid)
            await self.join_room(room_id, sid)

    @inject    
    async def on_try_hit(self, sid, data, game: Annotated[BoardDTO, Depends()]):
        # get the room state from Redis as a JSON object
        room_state = rj.get_json("room:{}".format(sid))
        # randomly broadcast a "hit" or "no hit" message to the room
        result = BoardShooterDTO().shoot(game, data.x, data.y)
        await self.send(room=sid, message=result.state)
        # update the room state in Redis
        room_state["state"] = result.state
        rj.set_json("room:{}".format(sid), room_state)

    @inject
    async def on_disconnect(self, sid, session: Annotated[SAGameSessionGateway, Depends()]):
        # get the room state from Redis as a JSON object
        room_state = rj.get_json("room:{}".format(sid))
        game_state = self.get_game_state(sid)
        if room_state:
            # remove the user from the room
            await self.leave_room(sid)
            # delete the room state from Redis
            rj.delete("room:{}".format(sid))
    

def setup_socketio(api_prefix: str, fastapi: FastAPI) -> AsyncServer:
    server = socketio.AsyncServer(cors_allowed_origins="*", cors_credentials=True, engineio_logger=False, )
    server.register_namespace(MyCustomNamespace('/game'))

    app = socketio.ASGIApp(server)

    fastapi.mount(api_prefix, app, name="Socket IO")
    return server
