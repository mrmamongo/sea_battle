from fastapi import APIRouter, Response, status
from ..infra/postgres/gateways import SAUserGateway
from jose import jwt, JWTError

router = APIRouter()

SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/auth")
async def auth(username: str):
    user_session = SAUserGateway()
    user_info = await user_session.get_by_username(username)
    if user_info:
        pass
    else:
        await user_session.create(username)
        access_token = create_access_token(
            data={"username": username}, expires_delta=datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        response.set_cookie(key="jwt_token", value=access_token, httponly=True)

    
