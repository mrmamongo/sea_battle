from datetime import datetime
from typing import Any

from pydantic import Field, field_validator

from src.presentation.scheme import BaseScheme


class GetGameSession(BaseScheme):
    session_id: str = Field(validation_alias="id")
    title: str
    state: str

    first_player: str = Field(validation_alias="first_player")
    second_player: str | None = Field(default=None, validation_alias="second_player")

    saved_state: dict | None = Field(default=None, validation_alias="saved_state")
    last_saved_state: datetime = Field(validation_alias="last_saved_state")

    @field_validator("session_id", mode="before")
    @classmethod
    def validate_session_id(cls, v: Any):
        return str(v)


class CreateGameSession(BaseScheme):
    session_id: str = Field(validation_alias="id")

    @field_validator("session_id", mode="before")
    @classmethod
    def validate_session_id(cls, v: Any):
        return str(v)
