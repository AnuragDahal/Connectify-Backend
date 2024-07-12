from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Response, Form, UploadFile, File, Query
from pydantic import EmailStr, constr
from typing import Annotated
from ..handlers.Auth.authhandler import AuthHandler
from ..handlers.User.userhandler import UserManager
from ..models import schemas
from ..handlers.Auth.emailHandler import EmailHandler
from ..config.dependencies import get_current_user
from ..utils.authutils import get_email_from_token
from ..handlers.exception import ErrorHandler
import re

router = APIRouter(prefix='/api/v1', tags=["Auth"])

PASSWORD_REGEX = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,16}$"


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup_user(
    name: str = Form(..., description="User's name"),
    email: EmailStr = Form(..., description="User's email"),
    password: str = Form(..., description="User's password"),
    image: UploadFile = File(None)
):
    # Manually validate the password
    if not re.match(PASSWORD_REGEX, password):
        return ErrorHandler.Error("Password validation failed")

    request = schemas.UserDetails(name=name, email=email, password=password)
    user = await UserManager.HandleNewUserCreation(request, image)
    return user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: OAuth2PasswordRequestForm = Depends()):
    user_in = await AuthHandler.HandleUserLogin(request)
    return user_in


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(res: Response, depends: str = Depends(get_current_user)):
    user_out = await AuthHandler.HandleUserLogout(res)
    return user_out


@router.post("/verify", status_code=status.HTTP_200_OK)
async def email_verification(email: Annotated[EmailStr, Query(..., description="Email to verify")], p: str = Depends(get_email_from_token), depends: str = Depends(get_current_user)):
    is_verified = await EmailHandler.HandleEmailVerification(email, p)
    return is_verified


@router.post("/otp", status_code=status.HTTP_200_OK)
async def otp_verification(
    otp: Annotated[str, Query(..., description="OTP to verify")],
    email: EmailStr = Depends(get_email_from_token),
    depends: str = Depends(get_current_user)
):
    is_verified = await EmailHandler.HandleOtpVerification(otp, email)
    return is_verified
