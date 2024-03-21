from typing import Protocol
from uuid import UUID

from src.application.common.dto import UpdateGameSession
from src.domain.models import GameSession, User


class UserGateway(Protocol):
    async def get_by_username(self, username: str) -> User | None:
        ...

    async def save(self, user: User) -> None:
        ...

    async def update(self, username: str, new_username: str) -> None:
        ...

    async def delete(self, user: User) -> None:
        ...


class GameSessionGateway(Protocol):
    async def get_by_player(self, username: str) -> list[GameSession]:
        ...

    async def save(self, game_session: GameSession) -> None:
        ...

    async def update(self, game_session: UpdateGameSession) -> None:
        ...

    async def delete(self, game_session_id: UUID) -> None:
        ...
