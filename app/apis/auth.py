from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Response, Query, Body
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
    name: Annotated[str, Body(..., description="User's name")],
    email: Annotated[str, Body(..., description="User's email")],
    password: Annotated[str, Body(..., description="User's password")],
):
    request = schemas.UserDetails(name=name, email=email, password=password)
    user = await UserManager.HandleNewUserCreation(request)
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
async def email_verification(email: Annotated[str, Query(..., description="Email to verify")], p: str = Depends(get_email_from_token), depends: str = Depends(get_current_user)):
    is_verified = await EmailHandler.HandleEmailVerification(email, p)
    return is_verified


@router.post("/otp", status_code=status.HTTP_200_OK)
async def otp_verification(
    otp: Annotated[str, Query(..., description="OTP to verify")],
    email: str = Depends(get_email_from_token),
    depends: str = Depends(get_current_user)
):
    is_verified = await EmailHandler.HandleOtpVerification(otp, email)
    return is_verified
