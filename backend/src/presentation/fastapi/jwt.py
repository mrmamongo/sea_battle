from jose import jwt, JWTError
from dishka.integrations.base import Depends
from dishka.integrations.fastapi import inject


class JWTGenerator():
    @inject
    def create_access_token(self, data: dict, secret_key: Annotated[SECRET_KEY, Depends()], algorithm: Annotated[ALGORITHM, Depends()]):
        to_encode = data.copy()
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt