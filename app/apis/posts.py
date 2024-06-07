from fastapi import APIRouter, status
from ..handlers.User.Posts.posthandler import PostsHandler
from ..models import schemas
from typing import List

router = APIRouter(prefix='/api/v1/posts', tags=["Posts"])


@router.post("/create", status_code=status.HTTP_200_OK)
async def create_post(request: schemas.Post):

    new_post = PostsHandler.HandlePostCreation(request)
    return new_post


@router.get("/read", response_model=List[schemas.Post], status_code=status.HTTP_200_OK)
async def get_posts():

    posts = PostsHandler.HandlePostReadings()
    return posts


@router.delete("/delete/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: str):

    post = PostsHandler.HandlePostDeletion(post_id)
    return post
