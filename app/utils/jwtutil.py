from datetime import datetime, timedelta, timezone
from ..utils.envutils import Environment
from jose import jwt
import os

env = Environment()
secret_key = env.secret_key
ALGORITHM = env.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = env.access_token_expire_minutes
TOKEN_TYPE = env.TOKEN_TYPE
TOKEN_KEY = env.TOKEN_KEY


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt
