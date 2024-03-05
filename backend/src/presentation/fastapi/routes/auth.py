from ../jwt import JWTGenerator
from dishka.integrations.base import Depends
from dishka.integrations.fastapi import inject

@inject
async def auth(username: str, user_session: Annotated[UserGateway, Depends()]):
    user_info = await user_session.get_by_username(username)
    if user_info:
        pass
    else:
        await user_session.create(username)
        access_token = JWTGenerator().create_access_token()
        response.set_cookie(key="jwt_token", value=access_token, httponly=True)