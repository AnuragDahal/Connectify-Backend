from fastapi import APIRouter, status, UploadFile, File, Form
from ..handlers.User.Posts.commentshandler import CommentsHandler
from ..models import schemas
from typing import List

router = APIRouter(prefix='/api/v1/posts/comments', tags=["Comments"])


@router.post("/create", status_code=status.HTTP_200_OK)
async def create_comment(request: schemas.Comments):

    new_comment = CommentsHandler.HandleCommentCreation(request)
    return new_comment


@router.get("/read", response_model=List[schemas.Comments], status_code=status.HTTP_200_OK)
async def get_comments():

    comments = CommentsHandler.HandleCommentReadings()
    return comments


@router.patch("/update", response_model=schemas.Comments, status_code=status.HTTP_200_OK)
async def update_comment(request: schemas.Comments, comment_id):

    updated_comment = CommentsHandler.HandleCommentUpdate(request, comment_id)
    return updated_comment


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_comment(comment_id):

    comment = CommentsHandler.HandleCommentDeletion(comment_id)
    return comment
