import json
from typing import Sequence
from uuid import UUID

import structlog
from adaptix import name_mapping, Retort
from adaptix.conversion import get_converter
from sqlalchemy import delete, insert, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dto import UpdateGameSession
from src.application.common.gateways import GameSessionGateway, UserGateway
from src.domain.models import GameSession, User
from src.infra.postgres.models import GameSessionModel, UserModel

logger = structlog.get_logger(__name__)


class SAGateway:
    def __init__(self, session: AsyncSession):
        self.session = session


class SAUserGateway(SAGateway, UserGateway):
    convert_to_domain = get_converter(UserModel, User)

    async def get_by_username(self, username: str) -> User | None:
        model = (
            await self.session.scalars(
                select(UserModel).where(UserModel.username == username)
            )
        ).one_or_none()
        if model is None:
            return None

        return SAUserGateway.convert_to_domain(model)

    async def save(self, user: User) -> None:
        try:
            await self.session.execute(insert(UserModel).values(username=user.username))
            await self.session.flush()
        except Exception as e:
            await logger.aerror("SA Exception", e)

    async def update(self, username: str, new_username: str) -> None:
        await self.session.execute(
            update(UserModel)
            .where(UserModel.username == username)
            .values(username=new_username)
        )
        await self.session.flush()

    async def delete(self, user: User) -> None:
        await self.session.execute(
            delete(UserModel).where(UserModel.username == user.username)
        )
        await self.session.flush()


class SAGameSessionGateway(SAGateway, GameSessionGateway):
    retort = Retort(recipe=[name_mapping(UpdateGameSession, omit_default=True)])

    async def get_by_player(self, username: str) -> list[GameSession]:
        models: Sequence[GameSessionModel] = (
            await self.session.scalars(
                select(GameSessionModel).where(
                    or_(
                        GameSessionModel.first_player == username,
                        GameSessionModel.second_player == username,
                    )
                )
            )
        ).all()
        return [
            GameSession(
                id=model.id,
                title=model.title,
                state=model.state,
                first_player=model.first_player,
                second_player=model.second_player,
                saved_state=json.loads(model.saved_state)
                if model.saved_state
                else None,
                last_saved_state=model.last_saved_state,
            )
            for model in models
        ]

    async def save(self, game_session: GameSession) -> None:
        try:
            await self.session.execute(
                insert(GameSessionModel).values(
                    id=game_session.id,
                    state=game_session.state,
                    first_player=game_session.first_player,
                    second_player=game_session.second_player,
                    saved_state=game_session.saved_state,
                    last_saved_state=game_session.last_saved_state,
                )
            )
            await self.session.flush()
        except Exception as e:
            await logger.aerror("SA Exception", e)

    async def update(self, game_session: UpdateGameSession) -> None:
        statement = update(GameSessionModel)

        for field, value in self.retort.dump(game_session).items():
            statement.values(**{field: value})

        await self.session.execute(statement)
        await self.session.flush()

    async def delete(self, game_session_id: UUID) -> None:
        await self.session.execute(
            delete(GameSessionModel).where(GameSessionModel.id == game_session_id)
        )
