from fastapi import Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from jose import jwt
from datetime import timedelta
from ...utils.envutils import Environment
from ..exception import ErrorHandler
from ...utils.jwtutil import create_access_token
from ...utils.passhashutils import Encryptor
from ..User.userhandler import Validate
from ...core.database import user_collection

env = Environment()
SECRET_KEY = env.SECRET_KEY
ALGORITHM = env.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = env.ACCESS_TOKEN_EXPIRE_MINUTES
TOKEN_TYPE = env.TOKEN_TYPE
TOKEN_KEY = env.TOKEN_KEY


class AuthHandler:
    @staticmethod
    async def HandleUserLogin(request: OAuth2PasswordRequestForm = Depends()):
        user_email = await user_collection.find_one({"email": request.username})
        if user_email and Encryptor.verify_password(request.password, user_email["password"]):
            access_token_expires = timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user_email["email"]}, expires_delta=access_token_expires)

            response = JSONResponse(
                content={"access_token": access_token,
                         "token_type": TOKEN_TYPE}
            )

            response.set_cookie(key=TOKEN_KEY, value=access_token,
                                expires=access_token_expires.total_seconds())

            return response
        return ErrorHandler.NotFound("User not found")

    @staticmethod
    async def HandleUserLogout(res: Response):
        try:
            res.delete_cookie(key=TOKEN_KEY)
            return {"message": "Logged out successfully"}
        except Exception as e:
            return ErrorHandler.Error(str(e))
