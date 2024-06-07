from fastapi import APIRouter, status
from ..handlers.User.Posts.posthandler import PostsHandler
from ..models import schemas

router = APIRouter(prefix='/api/v1/posts', tags=["Posts"])


@router.post("/create", status_code=status.HTTP_200_OK)
async def create_post(request: schemas.Post):

    new_post = PostsHandler.HandlePostCreation(request)
    return new_post
