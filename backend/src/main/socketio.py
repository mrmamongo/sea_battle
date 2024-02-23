import socketio
import uuid
import json
import redis
import redisjson as rj

from functools import lru_cache
from fastapi import FastAPI
from socketio import AsyncServer, AsyncNamespace, async_mode
from sanic import Sanic
from sanic.response import text
from ../infra/postgres/gateways import SAGameSessionGateway

# initialize a global Redis connection
r = redis.Redis()

class GameNamespace(AsyncNamespace):
    @lru_cache(maxsize=128)
    def get_game_state(self, game_id):
        # get the game state from Redis as a JSON object
        game_state = rj.get_json(game_id)
        return game_state

    async def on_game_start(self, sid, data):
        game_session = SAGameSessionGateway()
        first_player_games = await game_session.get_by_first_player(sid)
        if first_player_games == 0:
            #Generate uuid
            self.game_id = str(uuid.uuid4())
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

    async def on_accept(self, sid, environ, room_id):
        game_sessiong = SAGameSessionGateway()
        # check if the user is already in a game room
        if await game_session.get_by_second_player(sid)
            # if so, send a message to the user to confirm they're already in a game
            await self.send(sid, "You are already in a game.", room=sid)
        #else join the room
        else:
            await self.join_room(room_id, sid)
            
    async def on_try_hit(self, sid, data):
        # get the room state from Redis as a JSON object
        room_state = rj.get_json("room:{}".format(sid))
        # randomly broadcast a "hit" or "no hit" message to the room
        result = random.choice(["hit", "no hit"])
        await self.send(room=sid, message=result)
        # update the room state in Redis
        room_state["state"] = result
        rj.set_json("room:{}".format(sid), room_state)

    async def on_disconnect(self, sid):
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

    app = socketio.ASGIApp(server)
    app.namespace("/game", GameNamespace)

    fastapi.mount(api_prefix, app, name="Socket IO")
    return server

if __name__ == "__main__":
    async_mode("sanic")
    app.run(host="0.0.0.0", port=8000)