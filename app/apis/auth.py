from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Response, Form, UploadFile, File, Query, Request
from typing import Annotated
from ..handlers.Auth.authhandler import AuthHandler
from ..handlers.User.userhandler import UserManager
from ..models import schemas
from ..handlers.Auth.emailHandler import EmailHandler
from ..config.dependencies import get_current_user
from ..utils.authutils import get_email_from_token
router = APIRouter(prefix='/api/v1', tags=["Auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup_user(
    name: Annotated[str, Form(..., description="User's name")],
    email: Annotated[str, Form(..., description="User's email")],
    password: Annotated[str, Form(..., description="User's password")],
    image: UploadFile = File(None)
):
    request = schemas.UserDetails(name=name, email=email, password=password)
    user = await UserManager.HandleNewUserCreation(request, image)
    return user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: OAuth2PasswordRequestForm = Depends()):
    user_in = await AuthHandler.HandleUserLogin(request)
    return user_in


@router.post("/logout")
async def logout(res: Response):
    user_out = await AuthHandler.HandleUserLogout(res)
    return user_out


@router.post("/verify", status_code=status.HTTP_200_OK)
async def email_verification(email: Annotated[str, Query(..., description="Email to verify")], p: str = Depends(get_email_from_token)):
    is_verified = await EmailHandler.HandleEmailVerification(email,p)
    return is_verified


@router.post("/otp", status_code=status.HTTP_200_OK)
async def otp_verification(
    otp: Annotated[str, Query(..., description="OTP to verify")],
    email: str = Depends(get_email_from_token),
):
    is_verified = await EmailHandler.HandleOtpVerification(otp, email)
    return is_verified
