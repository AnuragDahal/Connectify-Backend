from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Response
from ..handlers.Auth.authhandler import AuthHandler
from ..handlers.User.userhandler import UserManager
from ..models import schemas
from ..handlers.Auth.emailHandler import EmailHandler

router = APIRouter(prefix='/api/v1', tags=["Auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED,)
async def Signup_User(req: schemas.User):

    user = UserManager.create(req)
    return user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: OAuth2PasswordRequestForm = Depends()):

    user_in = AuthHandler.login(request)
    return user_in


@router.post("/logout")
async def logout(res: Response):

    user_out = AuthHandler.logout(res)
    return user_out


@router.post("/verify", status_code=status.HTTP_200_OK)
async def email_verification(email: str):
    handler = EmailHandler()
    isVerified = handler.HandleEmailVerification(email)
    return isVerified


@router.post("/otp", status_code=status.HTTP_200_OK)
async def otp_verification(otp: str, email: str):

    isVerified = EmailHandler.HandleOtpVerification(otp, email)
    return isVerified
