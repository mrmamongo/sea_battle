import structlog

from src.presentation.socketio_presenters.di import DishkaAsyncNamespace
from src.presentation.socketio_presenters.scheme import EnterGame

logger = structlog.getLogger(__name__)

class GameNamespace(DishkaAsyncNamespace):

    async def on_enter_game(self, sid, environ, game_id: str, game_session_gateway: RedisGameSessionGateway):
        await logger.ainfo("entering game", sid, environ, game_id)

        await self.enter_room(sid, f"game:{game_id}")


    async def on_disconnect(self, sid, environ):
        await self.close_room()
