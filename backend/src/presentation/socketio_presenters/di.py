import asyncio

from dishka import AsyncContainer
from dishka.integrations.base import wrap_injection
from socketio import AsyncNamespace


class DishkaAsyncNamespace(AsyncNamespace):
    def __init__(self, namespace: str, container: AsyncContainer) -> None:
        self.dishka_container = container
        super().__init__(namespace)

    async def trigger_event(self, event, *args):
        handler_name = "on_" + event
        if hasattr(self, handler_name):
            try:
                return await wrap_injection(
                func=getattr(self, handler_name),
                remove_depends=True,
                container_getter=lambda _, p: self.dishka_container,
                is_async=True,
            )(*args)
            except asyncio.CancelledError:  # pragma: no cover
                return None
