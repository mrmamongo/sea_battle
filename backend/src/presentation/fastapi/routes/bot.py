from typing import Annotated

from aiogram import Bot, Dispatcher
from dishka.integrations.base import Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

router = APIRouter()


@inject
async def handle_update(
    update: dict, bot: Annotated[Bot, Depends()], dp: Annotated[Dispatcher, Depends()]
):
    await dp.feed_raw_update(bot, update)
