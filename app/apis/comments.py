from fastapi import APIRouter, status, UploadFile, File, Form
from ..handlers.User.Posts.commentshandler import CommentsHandler
from ..models import schemas
from typing import List

router = APIRouter(prefix='/api/v1/post/comments', tags=["Comments"])


@router.post("/create", status_code=status.HTTP_200_OK)
async def create_comment(request: schemas.Comments):

    new_comment = CommentsHandler.HandleCommentCreation(request)
    return new_comment


@router.get("/read", response_model=List[schemas.Comments], status_code=status.HTTP_200_OK)
async def get_comments():

    comments = CommentsHandler.HandleCommentReadings()
    return comments
