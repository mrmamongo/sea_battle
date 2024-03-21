import tomllib
from dataclasses import dataclass, field
from enum import Enum
from functools import cache
from logging import DEBUG
from pathlib import Path

from adaptix import Retort


@dataclass(slots=True)
class ApiConfig:
    host: str
    port: int

    # templates_dir: str
    workers: int = 1
    cors_origins: list[str] = field(default_factory=list)
    allow_headers: list[str] = field(default_factory=list)
    allow_methods: list[str] = field(default_factory=list)
    allow_credentials: bool = True


class StorageType(Enum):
    redis = "redis"
    inmemory = "inmemory"


@dataclass(slots=True)
class TelegramConfig:
    token: str
    webhook_base: str | None = None
    storage_args: dict[str, str] | None = None
    storage: StorageType = StorageType.inmemory


@dataclass(slots=True)
class DatabaseConfig:
    dsn: str


@dataclass(slots=True)
class LoggingConfig:
    level: str = DEBUG
    human_readable_logs: bool = True


@dataclass(slots=True)
class RedisConfig:
    url: str


@dataclass(slots=True)
class Config:
    api: ApiConfig = field(default_factory=ApiConfig)
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)


@cache
def get_config(config_path: Path) -> Config:
    retort = Retort()

    with open(config_path, "rb") as f:
        return retort.load(tomllib.load(f), Config)
