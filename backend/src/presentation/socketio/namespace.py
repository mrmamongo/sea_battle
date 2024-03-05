from src.presentation.socketio.di import DishkaAsyncNamespace, inject
from socketio import AsyncServer, AsyncNamespace, async_mode
from src.infra.postgres.gateways import SAGameSessionGateway
from types import Annotated
from src.game_logic.game import Game
from functools import lru_cache
from redis.asyncio.client import Redis

from dishka.integrations.base import Depends
from dishka.integrations.fastapi import inject

import uuid

class Namespace(DishkaAsyncNamespace):
    @inject
    async def on_connect(self, sid, environ, ):
        await self.enter_room(sid)

class GameNamespace(AsyncNamespace):

    @lru_cache(maxsize=128)
    @inject
    async def get_game_state(self, game_id, redis_session: Annotated[Redis, Depends()]):
        return await redis_session.get(game_id)

    @inject
    async def set_game_state(self, room_id, game: Game, redis_session: Annotated[Redis, Depends()]):
        return await redis_session.set(room_id, game)
    
    @inject
    async def delete_game_state(self, room_id, redis_session: Annotated[Redis, Depends()]):
        return await redis_session.delete(room_id)

    @inject
    async def on_connect(self, sid, environ, game_session: Annotated[SAGameSessionGateway, Depends()], game: Annotated[Game, Depends()]):
        first_player = environ['HTTP_USERNAME']
        self.set_game_state(sid, game)
        await game_session.create(id=sid, first_player=first_player, state='Created')

    @inject
    async def on_accept(self, sid, data, room_id, game_session: Annotated[SAGameSessionGateway, Depends()]):
        second_player = data['second_player']
        # check if the user is already in a game room
        if await game_session.get_by_second_player(second_player):
            # if so, send a message to the user to confirm they're already in a game
            await self.emit("You are already in a game.", room=sid)
        #else join the room
        else:
            await game_session.update(room_id, state='Started', second_player=second_player)
            await self.enter_room(sid=sid, room=room_id)

    @inject    
    async def on_try_hit(self, sid, data, game_session: Annotated[SAGameSessionGateway, Depends()]):
        game = self.get_game_state(sid)
        if game.game_state == 'Ended':
            await self.emit("Game is already ended!", room=sid)
            await game_session.update(sid, state='Stoped')
        else:
            game.shoot(data.x, data.y)
            self.set_game_state(sid, game)
    
    @inject
    async def on_disconnect(self, sid, game_session: Annotated[SAGameSessionGateway, Depends()]):
        await self.leave_room(sid)
        await self.close_room(sid)

        await game_session.update(sid, state='Deleted')
