from fastapi import APIRouter, status, Form
from ..handlers.User.Posts.commentshandler import CommentsHandler
from ..models import schemas
from typing import List

router = APIRouter(prefix='/api/v1/posts/comments', tags=["Comments"])


@router.post("/create", status_code=status.HTTP_200_OK)
async def create_comment(
    post_id: str = Form(...),
    content: str = Form(...),
    commented_by: str = Form(...)
):
    request = schemas.Comments(
        post_id=post_id, commented_by=commented_by, comment=content)
    new_comment = await CommentsHandler.HandleCommentCreation(request)
    return new_comment


@router.get("/read", response_model=List[schemas.Comments], status_code=status.HTTP_200_OK)
async def get_comments():
    comments = await CommentsHandler.HandleCommentReadings()
    return comments


@router.patch("/update", response_model=schemas.Comments, status_code=status.HTTP_200_OK)
async def update_comment(
    comment_id: str,
    post_id: str = Form(...),
    commented_by: str = Form(...),
    content: str = Form(...)
):
    request = schemas.Comments(
        post_id=post_id, commented_by=commented_by, comment=content)
    updated_comment = await CommentsHandler.HandleCommentUpdate(request, comment_id)
    return updated_comment


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_comment(comment_id: str):
    comment = await CommentsHandler.HandleCommentDeletion(comment_id)
    return comment
