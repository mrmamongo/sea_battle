from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.gateways import GameSessionGateway
from src.application.common.usecase import Usecase
from src.domain.models import GameSession
from src.domain.services import GameSessionService


class CreateGame(Usecase[str, GameSession]):
    def __init__(
        self,
        session: AsyncSession,
        game_session_gateway: GameSessionGateway,
        game_session_service: GameSessionService,
    ) -> None:
        self.session = session
        self.game_session_service = game_session_service
        self.game_session_gateway = game_session_gateway

    async def __call__(self, data: str) -> GameSession:
        async with self.session.begin():
            session = self.game_session_service.create_game_session(data)

            await self.game_session_gateway.save(session)

            return session
