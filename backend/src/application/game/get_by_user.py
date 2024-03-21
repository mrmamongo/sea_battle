from src.application.common.gateways import GameSessionGateway
from src.application.common.usecase import Usecase
from src.domain.models import GameSession


class GetGamesByUser(Usecase):
    def __init__(
        self,
        game_session_gateway: GameSessionGateway,
    ) -> None:
        self.game_session_gateway = game_session_gateway

    async def __call__(self, username: str) -> list[GameSession]:
        return await self.game_session_gateway.get_by_player(username)
