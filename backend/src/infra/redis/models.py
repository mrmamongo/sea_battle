import enum
from dataclasses import dataclass


@dataclass
class UserSession:
    token: str
    username: str


class UserTurn(enum.StrEnum):
    first = "first"
    second = "second"


@dataclass
class GameSession:
    game_id: str
    players: tuple[str, str]
    boards: tuple
    turn: UserTurn
