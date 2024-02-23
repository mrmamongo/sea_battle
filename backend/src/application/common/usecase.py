from typing import Generic, TypeVar
from fastapi import APIRouter, Response, status
from ..infra/postgres/gateways import SAUserGateway

router = APIRouter()

InputDTO = TypeVar("InputDTO", covariant=True)
OutputDTO = TypeVar("OutputDTO", contravariant=True)



class Usecase(Generic[InputDTO, OutputDTO]):
    router = APIRouter()
    async def __call__(self, data: InputDTO) -> OutputDTO:
        pass
