from fastapi import APIRouter, status, UploadFile, File, Form, Query, Path, Depends
from typing import List, Optional
from ..handlers.User.Posts.posthandler import PostsHandler
from ..models import schemas
from ..config.dependencies import get_current_user
from ..utils.authutils import get_email_from_token

router = APIRouter(prefix='/api/v1/posts',
                   tags=["Posts"], dependencies=[Depends(get_current_user)])


@router.post("/create", status_code=status.HTTP_200_OK)
async def create_post(
    title: str = Form(...),
    content: Optional[str] = Form(None),
    posted_by: str = Depends(get_email_from_token),
    image: List[UploadFile] = File([])
):
    request = schemas.Post(title=title, content=content, posted_by=posted_by)
    new_post = await PostsHandler.HandlePostCreation(request, image)
    return new_post


@router.get("/read/public", response_model=List[schemas.Post], status_code=status.HTTP_200_OK)
async def get_posts():
    posts = await PostsHandler.HandlePublicPostReadings()
    return posts


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_post(post_id: str = Query(...)):
    post = await PostsHandler.HandlePostDeletion(post_id)
    return post


@router.get("/{email}", response_model=List[schemas.Post], status_code=status.HTTP_200_OK)
async def get_user_posts(email: str = Path(...)):
    posts = await PostsHandler.HandleUserPostsRetrieval(email)
    return posts


@router.post("/image", status_code=status.HTTP_200_OK)
async def upload_post_image(
    post_id: str = Form(...),
    file: UploadFile = File(...)
):
    upload_file = await PostsHandler.HandlePostImageUpload(post_id, file)
    return upload_file


@router.patch("/update", response_model=schemas.PostUpdate, status_code=status.HTTP_200_OK)
async def update_post(
    post_id: str = Query(...),
    title: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    images: List[UploadFile] = File([])
):
    request = schemas.PostUpdate(title=title, content=content)
    updated_post = await PostsHandler.HandlePostUpdate(request, post_id, images)
    return updated_post


@router.patch("/like", status_code=status.HTTP_200_OK)
async def like_post(
    post_id: str = Query(...),
    liked_by_user: str = Form(...)
):
    like = await PostsHandler.HandlePostLike(post_id, liked_by_user)
    return like


@router.get("/like/count", status_code=status.HTTP_200_OK)
async def get_likes_count(post_id: str = Query(...)):
    likes_count = await PostsHandler.HandleLikesCounts(post_id)
    return likes_count


@router.get("/friend/show", response_model=List[schemas.Post], status_code=status.HTTP_200_OK)
async def get_post_of_friend(friend_email: str = Query(...), user_logged_in: str = Depends(get_email_from_token)):
    print(user_logged_in)
    posts = await PostsHandler.HandleFriendPostsRetrieval(
        friend_email, user_logged_in)
    return posts


@router.put("/privacy", status_code=status.HTTP_200_OK)
async def update_post_privacy(

    post_id: str = Query(...),
    privacy: str = Query(...),
    email: str = Depends(get_email_from_token)
):
    post = await PostsHandler.HandlePostPrivacyUpdate(post_id, privacy, email)
    return post
