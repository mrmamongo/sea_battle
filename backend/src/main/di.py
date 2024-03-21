from typing import AsyncIterable

from aiogram import Bot, Dispatcher
from dishka import from_context, provide, Provider, Scope
from fastapi import HTTPException, Request
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from starlette import status

from src.application.common.gateways import GameSessionGateway, UserGateway
from src.application.game.create_game import CreateGame
from src.application.game.get_by_user import GetGamesByUser
from src.application.user.get_or_create import GetOrCreateUser
from src.config import Config
from src.domain.services import GameSessionService, UserService
from src.infra.postgres.gateways import SAGameSessionGateway, SAUserGateway
from src.infra.postgres.models import BaseModel
from src.infra.redis.gateways import RedisUserSessionGateway
from src.infra.redis.models import UserSession


class DIProvider(Provider):
    def __init__(
        self,
        config: Config,
        bot: Bot | None = None,
        dispatcher: Dispatcher | None = None,
    ):
        self.config = config
        self.bot = bot
        self.dispatcher = dispatcher
        super().__init__()

    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncIterable[AsyncEngine]:
        engine: AsyncEngine = create_async_engine(self.config.database.dsn)
        async with engine.begin() as conn:  # TODO: Сделать нормальные миграции
            await conn.run_sync(BaseModel.metadata.create_all)

        yield engine

        await engine.dispose()

    @provide(scope=Scope.APP)
    async def get_session_maker(
        self, engine: AsyncEngine
    ) -> AsyncIterable[async_sessionmaker[AsyncSession]]:
        yield async_sessionmaker(engine, autoflush=False, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    async def get_redis(self) -> AsyncIterable[Redis]:
        yield Redis.from_url(self.config.redis.url)

    provide_game_session_service = provide(
        scope=Scope.REQUEST, source=GameSessionService
    )
    provide_game_session_gateway = provide(
        scope=Scope.REQUEST, source=SAGameSessionGateway, provides=GameSessionGateway
    )

    provide_user_gateway = provide(
        scope=Scope.REQUEST, source=SAUserGateway, provides=UserGateway
    )
    provide_user_service = provide(scope=Scope.REQUEST, source=UserService)

    provide_redis_user_session_gateway = provide(
        scope=Scope.REQUEST, source=RedisUserSessionGateway
    )

    @provide(scope=Scope.REQUEST)
    async def auth_dependency(
        self, request: Request, session_gateway: RedisUserSessionGateway
    ) -> AsyncIterable[UserSession]:
        session_cookie = request.cookies.get("session")
        if session_cookie is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="No cookies provided"
            )
        session = await session_gateway.get_by_token(session_cookie)
        if session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session"
            )
        yield session


class UsecaseProvider(Provider):
    provide_get_or_create = provide(scope=Scope.REQUEST, source=GetOrCreateUser)
    provide_create_game = provide(scope=Scope.REQUEST, source=CreateGame)
    provide_get_game_by_user = provide(scope=Scope.REQUEST, source=GetGamesByUser)
