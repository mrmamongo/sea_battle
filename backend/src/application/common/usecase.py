from typing import Generic, TypeVar

class Usecase(Generic[InputDTO, OutputDTO]):
    async def __call__(self, data: InputDTO) -> OutputDTO:
        pass
