from fastapi import APIRouter, status,  Depends, Response, UploadFile, File, Form, Query, Path
from ..handlers.User.userhandler import UserManager
from ..handlers.User.uploadhandler import UploadManager
from typing import List
from ..config.dependencies import get_current_user
from ..models import schemas
from ..utils.authutils import get_email_from_token

router = APIRouter(prefix='/api/v1', tags=["Users"],
                   )


@router.get("/user", response_model=List[schemas.UserDetails], status_code=status.HTTP_200_OK,)
async def read_user():

    user = await UserManager.read()
    return user


@router.patch("/update/{old_email}", dependencies=[Depends(get_current_user)], response_model=schemas.UserSignUp, status_code=status.HTTP_200_OK)
async def update_user(new_email: str = Form(..., description="Enter the new email"), old_email: str = Depends(get_email_from_token), password: str = Form(..., description="Enter your password to update the email")):

    update_data = await UserManager.update(old_email, new_email, password)
    return update_data


@router.delete("/delete", dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK,)
async def delete_user(res: Response, email: str = Depends(get_email_from_token), depends=Depends(get_current_user)):

    user = await UserManager.delete(email, res)
    return user


@router.post("/profile", dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
async def upload_profile_pic(img: UploadFile = File(...), email: str = Depends(get_email_from_token)):

    img_upload = await UploadManager.HandleUploadProfilePic(email, img)
    return img_upload
