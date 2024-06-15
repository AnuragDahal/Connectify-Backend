from fastapi import APIRouter, status, Request, Depends, Response, UploadFile, File
from ..handlers.User.userhandler import UserManager
from ..handlers.User.uploadhandler import UploadManager
from ..handlers.User.Posts.posthandler import PostsHandler
from typing import List
from ..config.dependencies import verify_token
from ..models import schemas
router = APIRouter(prefix='/api/v1', tags=["Users"])


@router.get("/user", response_model=List[schemas.UserDetails], status_code=status.HTTP_200_OK,)
async def read_user():

    user = await UserManager.read()
    return user


@router.patch("/update/{old_email}", response_model=schemas.UserSignUp, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_token)])
async def update_user(old_email: str, request: Request, new_email: schemas.UpdateUserEmail):

    update_data = await UserManager.update(old_email, request, new_email)
    return update_data


@router.delete("/delete", status_code=status.HTTP_200_OK,)
async def delete_user(request: Request, res: Response, depends=Depends(verify_token)):

    user = await UserManager.delete(request, res)
    return user


@router.post("/profile", status_code=status.HTTP_200_OK)
async def upload_profile_pic(email: str, img: UploadFile = File(...)):

    img_upload =await UploadManager.HandleUploadProfilePic(email, img)
    return img_upload
