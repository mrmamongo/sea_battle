from typing import Protocol

from uuid import UUID


class UserGateway(Protocol):
    async def get_by_username(self, username: str):
        ...

    async def create(self, username: str) -> None:
        ...

    async def update(self, username: str, new_username: str) -> None:
        ...

    async def delete(self, username: str) -> None:
        ...

class GameGateway(Protocol):
    async def get_by_uuid(self, uuid: UUID):
        ...
    
    async def create(self, state: str, first_player: str):
        ...

    async def get_by_first_player(self, uuid: str):
        ...
    
    async def get_by_second_player(self, uuid: str):
        ...

    async def create(self, uuid: str, state: str, first_player: str):
        ...
    
    async def update(self, uuid: UUID, state=None, second_player=None, saved_state=None, last_saved_state=None):
        ...
    
    async def delete(self):
        ...