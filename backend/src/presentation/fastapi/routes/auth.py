from typing import Annotated

from dishka.integrations.fastapi import inject
from fastapi import Cookie, Response

from dishka.integrations.base import Depends
from fastapi import APIRouter
from starlette import status

from src.application.user.get_or_create import GetOrCreateUser
from src.infra.redis.gateways import RedisUserSessionGateway

router = APIRouter(prefix="/auth")


@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def get_token(
    username: str,
    response: Response,
    session_repo: Annotated[RedisUserSessionGateway, Depends()],
    usecase: Annotated[GetOrCreateUser, Depends()],
) -> None:
    user = await usecase(username)
    session = await session_repo.create_session(user.username)
    response.set_cookie(key="session", value=session.token, httponly=True, secure=True)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def logout(
    response: Response,
    session_repo: Annotated[RedisUserSessionGateway, Depends()],
    session: Annotated[str | None, Cookie()] = None,
) -> None:
    if session is None:
        return
    response.delete_cookie(key="session", httponly=True, secure=True)
    await session_repo.delete_session(session)
