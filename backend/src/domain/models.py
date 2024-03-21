from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    username: str


@dataclass
class GameSession:
    id: UUID
    title: str
    state: str

    first_player: str
    second_player: str | None

    saved_state: dict | None
    last_saved_state: datetime
