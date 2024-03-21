from typing import Annotated, List

from dishka.integrations.base import Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.application.game.create_game import CreateGame
from src.application.game.get_by_user import GetGamesByUser
from src.domain.models import GameSession
from src.infra.redis.models import UserSession
from src.presentation.fastapi.scheme import CreateGameSession, GetGameSession

router = APIRouter(prefix="/game")


@router.get("/", response_model=List[GetGameSession])
@inject
async def get_games(
    user_session: Annotated[UserSession, Depends()],
    usecase: Annotated[GetGamesByUser, Depends()],
) -> list[GameSession]:
    sessions = await usecase(user_session.username)
    return sessions


@router.post("/create", response_model=CreateGameSession)
@inject
async def create_game(
    usecase: Annotated[CreateGame, Depends()],
    user_session: Annotated[UserSession, Depends()],
) -> GameSession:
    return await usecase(user_session.username)
