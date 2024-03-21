from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.gateways import UserGateway
from src.application.common.usecase import Usecase
from src.domain.models import User
from src.domain.services import UserService


class GetOrCreateUser(Usecase[str, User]):
    def __init__(
        self,
        session: AsyncSession,
        user_gateway: UserGateway,
        user_service: UserService,
    ) -> None:
        self.session = session
        self.user_gateway = user_gateway
        self.user_service = user_service

    async def __call__(self, data: str) -> User:
        async with self.session.begin():
            user = await self.user_gateway.get_by_username(data)
            if user is None:
                user = self.user_service.create_user(data)
                await self.user_gateway.save(user)

            return user
