from typing import AsyncIterable

from aiogram import Bot, Dispatcher
from dishka import provide, Provider, Scope
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, AsyncSession, create_async_engine
from src.infra.postgres.gateways import SAGameSessionGateway, SAUserGateway
from src.game_logic.game import Game

from src.application.handle_update import HandleUpdate
from src.config import Config


class DIProvider(Provider):
    def __init__(self, config: Config, bot: Bot, dispatcher: Dispatcher):
        self.config = config
        self.bot = bot
        self.dispatcher = dispatcher
        super().__init__()

    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncIterable[AsyncEngine]:
        engine: AsyncEngine = create_async_engine(self.config.database.dsn)
        yield engine

        await engine.dispose()

    @provide(scope=Scope.APP)
    async def get_session_maker(self, engine: AsyncEngine) -> AsyncIterable[async_sessionmaker]:
        yield async_sessionmaker(engine, autoflush=False, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    async def get_redis(self) -> AsyncIterable[Redis]:
        yield Redis.from_url(self.config.redis.url)

    @provide(scope=Scope.REQUEST)
    async def get_game_session(self) -> AsyncIterable[SAGameSessionGateway]:
        yield SAGameSessionGateway()
    
    @provide(scope=Scope.REQUEST)
    async def get_user_session(self) -> AsyncIterable[SAUserGateway]:
        yield SAUserGateway()
    
    @provide(scope=Scope.REQUEST)
    async def get_game(self) -> AsyncIterable[Game]:
        yield Game(size=10, amount_3d=0, amount_2d=2, amount_1d=3)

class UsecaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_dispatch_update(self, bot: Bot, dp: Dispatcher) -> AsyncIterable[HandleUpdate]:
        yield HandleUpdate(bot=bot, dp=dp)
