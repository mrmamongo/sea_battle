from adaptix import Retort
from redis.asyncio.client import Redis

from src.infra.redis.models import GameSession, UserSession, UserTurn
from src.infra.redis.token_generator import generate_token


class RedisGateway:
    def __init__(self, session: Redis):
        self.session = session


class RedisUserSessionGateway(RedisGateway):
    retort = Retort()

    async def get_by_token(self, token: str) -> UserSession | None:
        session = await self.session.json().get(f"session:{token}")
        if session is None:
            return None

        return self.retort.load(session, UserSession)

    async def create_session(self, username: str) -> UserSession:
        session = UserSession(username=username, token=generate_token(username))
        await self.session.json().set(
            f"session:{session.token}", ".", self.retort.dump(session)
        )

        return session

    async def delete_session(self, token: str) -> None:
        await self.session.json().delete(f"session:{token}")


class RedisGameSessionGateway(RedisGateway):
    retort = Retort()

    async def get_by_id(self, game_id: str) -> GameSession | None:
        session = self.session.json().get(f"game:{game_id}")
        if session is None:
            return None

        return self.retort.load(session, GameSession)

    async def create_session(self, game_id: str, players: tuple[str, str], turn: UserTurn) -> GameSession:
        session = GameSession(game_id=game_id, players=players, turn=turn, boards=())
        await self.session.json().set(
            f"game:{session.game_id}", ".", self.retort.dump(session)
        )

        return session
