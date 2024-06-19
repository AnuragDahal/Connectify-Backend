from fastapi import Request, HTTPException
from jose import jwt, JWTError
from typing import Callable
from functools import wraps
from .envutils import Environment
env = Environment()


def validate_headers(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # The first argument should be the request
        req = args[0] if args else None
        if not isinstance(req, Request):
            raise HTTPException(
                status_code=400, detail="The first argument must be a Request instance")

        # Get the email from the request headers
        auth_header = req.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            try:
                payload = jwt.decode(token, env.SECRET_KEY,
                                     algorithms=[env.ALGORITHM])
                email = payload.get('sub')
            except JWTError:
                raise HTTPException(status_code=401, detail="Invalid Token")
        else:
            raise HTTPException(
                status_code=401, detail="Could not find the appropriate headers")

        # Call the original function with the email as the first argument
        return await func(email, *args, **kwargs)

    return wrapper
