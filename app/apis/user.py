from fastapi import APIRouter, status, Request, Depends, Response, UploadFile, File
from ..handlers.User.userhandler import UserManager
from ..handlers.User.uploadhandler import UploadManager
from typing import List
from ..config.dependencies import verify_token, get_current_user
from ..models import schemas
from ..utils.authutils import get_email_from_token

router = APIRouter(prefix='/api/v1', tags=["Users"],
                   )


@router.get("/user", response_model=List[schemas.UserDetails], status_code=status.HTTP_200_OK,)
async def read_user():

    user = await UserManager.read()
    return user


@router.patch("/update/{old_email}", dependencies=[Depends(get_current_user), Depends(verify_token)], response_model=schemas.UserSignUp, status_code=status.HTTP_200_OK)
async def update_user(old_email: str, request: Request, new_email: schemas.UpdateUserEmail):

    update_data = await UserManager.update(old_email, request, new_email)
    return update_data


@router.delete("/delete", dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK,)
async def delete_user(request: Request, res: Response, depends=Depends(get_current_user)):

    user = await UserManager.delete(request, res)
    return user


@router.post("/profile", dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
async def upload_profile_pic(img: UploadFile = File(...), email: str = Depends(get_email_from_token)):

    img_upload = await UploadManager.HandleUploadProfilePic(email, img)
    return img_upload
