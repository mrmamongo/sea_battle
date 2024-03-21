import datetime
import uuid

from src.domain.models import GameSession, User


class UserService:
    @staticmethod
    def create_user(username: str) -> User:
        return User(username=username)


class GameSessionService:
    @staticmethod
    def create_game_session(username: str) -> GameSession:
        return GameSession(
            id=uuid.uuid4(),
            state="created",
            first_player=username,
            last_saved_state=datetime.datetime.now(),
            second_player=None,
            saved_state=None,
        )
