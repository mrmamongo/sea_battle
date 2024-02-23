from typing import Generic, TypeVar
from fastapi import APIRouter, Response, status
from ..infra/postgres/gateways import SAUserGateway
from jose import jwt, JWTError
from dishka.integrations.base import Depends
from dishka.integrations.fastapi import inject

router = APIRouter()

InputDTO = TypeVar("InputDTO", covariant=True)
OutputDTO = TypeVar("OutputDTO", contravariant=True)


class JWTGenerator():
    SECRET_KEY = ""
    ALGORITHM = "HS256"
    
    def create_access_token(self, data: dict):
        to_encode = data.copy()
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

class Usecase(Generic[InputDTO, OutputDTO]):
    router = APIRouter()
    async def __call__(self, data: InputDTO) -> OutputDTO:
        pass

    @router.post("/auth")
    @inject
    async def auth(username: str, user_session: Annotated[SAUserGateway, Depends()]):
        user_session = SAUserGateway()
        user_info = await user_session.get_by_username(username)
        if user_info:
            pass
        else:
            await user_session.create(username)
            access_token = JWTGenerator().create_access_token()
            response.set_cookie(key="jwt_token", value=access_token, httponly=True)