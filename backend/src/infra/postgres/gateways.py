import structlog
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.gateways import UserGateway, GameGateway
from src.infra.postgres.models import UserModel, GameSessionModel
from uuid import UUID

import time


logger = structlog.get_logger(__name__)


class SAGateway:
    def __init__(self, session: AsyncSession):
        self.session = session

class SAUserGateway(SAGateway, UserGateway):
    async def get_by_username(self, username: str):
        return (
            await self.session.execute(
                select(UserModel).where(UserModel.username == username)
            )
        ).one_or_none()

    async def create(self, username: str) -> None:
        model = UserModel(username=username)

        try:
            self.session.add(model)
            await self.session.flush()
        except Exception as e:
            await logger.aerror("SA Exception", e)

    async def update(self, username: str, new_username: str) -> None:
        await self.session.execute(
            update(UserModel)
            .where(UserModel.username == username)
            .values(username=new_username)
        )

    async def delete(self, username: str) -> None:
        model = self.session.get(UserModel, username)
        if model is None:
            return

        await self.session.delete(model)


class SAGameSessionGateway(SAGateway, GameGateway):
    async def get_by_uuid(self, uuid: str):
        return (
            await self.session.execute(
                select(GameSessionModel).where(GameSessionModel.id == uuid)
            ).one_or_none()
        )
    
    async def get_by_first_player(self, uuid: str):
        return (
            await self.session.execute(
                select(GameSessionModel).where(GameSessionModel.first_player == uuid)
            ).one_or_none()
        )

    async def get_by_second_player(self, uuid: str):
        return (
            await self.session.execute(
                select(GameSessionModel).where(GameSessionModel.second_player == uuid)
            ).one_or_none()
        )

    async def create(self, uuid: str, state: str, first_player: str) -> None:
        last_saved_state = time.now()
        model = GameSessionModel(state, first_player, last_saved_state)

        try:
            self.session.add(model)
            await self.session.flush()
        except Exception as e:
            await logger.aerror("SA Exception", e)

    async def update(self, uuid: str, state=None, second_player=None, saved_state=None, last_saved_state=None) -> None:
        query = update(GameSessionModel).where(GameSessionModel.id == uuid)
        if state:
            query = query.values(state=state)
        if second_player:
            query = query.values(second_player=second_player)
        if saved_state:
            query = query.values(saved_state=saved_state)
        if last_saved_state:
            query = query.values(last_saved_state=last_saved_state)
        try:
            self.session.execute(query)
            await self.session.flush()
        except Exception as e:
            await logger.aerror("SA Exception", e)

    async def delete(self, uuid: str) -> None:
        model = self.session.get(GameSessionModel, uuid)
        if model is None:
            return
        await self.session.delete(model)
        