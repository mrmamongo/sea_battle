import datetime
from typing import Optional
from uuid import UUID

import sqlalchemy
from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    pass


class UserModel(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(primary_key=True, unique=True)
    token: Mapped[str] = mapped_column(unique=True)


class GameSessionModel(BaseModel):
    __tablename__ = "game_sessions"

    id: Mapped[UUID] = mapped_column(sqlalchemy.UUID(as_uuid=True), primary_key=True)
    state: Mapped[str] = mapped_column()

    first_player: Mapped[str] = mapped_column(ForeignKey("users.username"))
    second_player: Mapped[Optional[str]] = mapped_column(
        ForeignKey("users.username"), nullable=True
    )

    saved_state: Mapped[Optional[JSON]] = mapped_column(nullable=True)
    last_saved_state: Mapped[datetime.datetime] = mapped_column()
