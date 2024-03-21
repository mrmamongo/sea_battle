import asyncio
import os
from pathlib import Path

import structlog
import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi

from src.config import Config, get_config
from src.infra.log import setup_logging
from src.main.di import DIProvider, UsecaseProvider
from src.main.pubsub import setup_socketio
from src.main.web import setup_fastapi
from src.presentation.socketio_presenters.namespace import GameNamespace

logger = structlog.get_logger(__name__)


async def run() -> None:
    config_path = Path(os.getenv("CONFIG_PATH"))
    if not config_path.exists():
        raise RuntimeError("Config file does not exist")

    config: Config = get_config(config_path)
    setup_logging(config.logging)

    await logger.ainfo("Initializing aiogram")
    # bot, dispatcher = await setup_dispatcher(config.telegram)
    providers = [DIProvider(config), UsecaseProvider()]
    container = make_async_container(*providers)

    # setup_dishka_aiogram(container, dispatcher)
    await logger.ainfo("Initializing fastapi")
    fastapi = setup_fastapi(config.api, config.telegram.token)
    await logger.ainfo("Starting service")
    socketio = setup_socketio("/api/v1", fastapi)
    socketio.register_namespace(GameNamespace("/game", container))

    setup_dishka_fastapi(container, fastapi)

    try:
        await uvicorn.Server(
            config=uvicorn.Config(
                app=fastapi,
                host=config.api.host,
                port=config.api.port,
                workers=config.api.workers,
                reload=True,
            )
        ).serve()
    finally:
        await container.close()


def main() -> None:
    try:
        asyncio.run(run())
        exit(os.EX_OK)
    except SystemExit:
        exit(os.EX_OK)
    except BaseException:
        logger.exception("Unexpected error occurred")
        exit(os.EX_SOFTWARE)


if __name__ == "__main__":
    main()
