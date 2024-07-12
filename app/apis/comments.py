from fastapi import APIRouter, status, Form, Depends, Query, Path
from ..handlers.User.Posts.commentshandler import CommentsHandler
from ..models import schemas
from typing import List
from pydantic import EmailStr
from ..config.dependencies import get_current_user
from ..utils.authutils import get_email_from_token

router = APIRouter(prefix='/api/v1/posts/comments', tags=["Comments"],
                   dependencies=[Depends(get_current_user)])


@router.post("/create", status_code=status.HTTP_200_OK)
async def create_comment(
    post_id: str = Form(...),
    content: str = Form(...),
    commented_by: str = Form(...),
    email: EmailStr = Depends(get_email_from_token)
):
    request = schemas.Comments(
        post_id=post_id, commented_by=commented_by, comment=content)
    new_comment = await CommentsHandler.HandleCommentCreation(request, email)
    return new_comment


@router.get("/read/{post_id}", response_model=List[schemas.Comments], status_code=status.HTTP_200_OK)
async def get_comments(post_id: str = Path(..., description="The post id of the post whose comments you want to read")):
    comments = await CommentsHandler.HandleCommentReadings(post_id)
    return comments


@router.patch("/update", response_model=schemas.Comments, status_code=status.HTTP_200_OK)
async def update_comment(
        comment_id: str = Query(...,
                                description="The comment id of the comment you want to update"),
        post_id: str = Form(...),
        commented_by: str = Depends(get_email_from_token),
        content: str = Form(...),
        email: EmailStr = Depends(get_email_from_token)):
    request = schemas.Comments(
        post_id=post_id, commented_by=commented_by, comment=content)
    updated_comment = await CommentsHandler.HandleCommentUpdate(request, comment_id, email)
    return updated_comment


@router.delete("/delete/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_post_comments(
        comment_id: str =
        Path(..., description="The comment id of the comment you want to delete"),
        email: EmailStr = Depends(get_email_from_token)):
    comment = await CommentsHandler.HandlePostCommentDeletion(comment_id, email)
    return comment


@router.delete("/deleteown/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_own_comments(comment_id: str =
                              Path(..., description="The comment id of the comment you want to delete"),
                              email: EmailStr = Depends(get_email_from_token)):
    comment = await CommentsHandler.HandleOwnCommentDeletion(comment_id, email)
    return comment
