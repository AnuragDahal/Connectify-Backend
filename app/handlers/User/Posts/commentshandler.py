from ....core.database import comments_collection, post_collection, user_collection
from ....models import schemas
from pymongo import ReturnDocument
from ...exception import ErrorHandler
from bson import ObjectId


class CommentsHandler:

    @staticmethod
    async def HandleCommentCreation(request: schemas.Comments):
        """
        Create a comment.
        """
        post = await post_collection.find_one({"_id": ObjectId(request.post_id)})
        if not post:
            return ErrorHandler.NotFound("Post not found")

        new_comment = await comments_collection.insert_one({**request.model_dump(exclude=None)})
        comment_id = str(new_comment.inserted_id)

        await post_collection.find_one_and_update(
            {"_id": ObjectId(request.post_id)},
            {"$addToSet": {'comments': comment_id}}
        )
        await user_collection.find_one_and_update(
            {"email": request.commented_by},
            {"$addToSet": {"comments_on_post": post["_id"]}}
        )

        await user_collection.find_one_and_update(
            {"email": request.commented_by},
            {"$addToSet": {"commented": comment_id}}
        )

        return {"id": str(new_comment.inserted_id)}

    @staticmethod
    async def HandleCommentReadings(post_id: str):
        """
        Get all the comments associated with the post .
        """
        post = await post_collection.find_one({"_id": ObjectId(post_id)})
        if post:
            comments = await comments_collection.find({"post_id": post_id}).to_list(length=100)
            if comments:
                return comments
            return ErrorHandler.NotFound("No comments found")
        return ErrorHandler.NotFound("No post found with the given post id")

    @staticmethod
    async def HandleCommentUpdate(request: schemas.Comments, comment_id: str):
        """Update the existing comment"""
        post = await post_collection.find_one({"_id": ObjectId(request.post_id)})
        if post:
            updated_comment = await comments_collection.find_one_and_update(
                {"_id": ObjectId(comment_id)},
                {"$set": request.model_dump(exclude={"comment_id"})},
                return_document=ReturnDocument.AFTER
            )
            if updated_comment:
                return updated_comment
            return ErrorHandler.NotFound("Failed to update comment")
        return ErrorHandler.NotFound("Post not found")

    @staticmethod
    async def HandleCommentDeletion(comment_id: str):
        """
        Delete a comment.
        """
        comment = await comments_collection.find_one({"_id": ObjectId(comment_id)})
        if comment:
            await post_collection.find_one_and_update(
                {"comments": comment_id},
                {"$pull": {"comments": comment_id}}
            )
            await comments_collection.find_one_and_delete({"_id": ObjectId(comment_id)})
            return {"message": f"Comment deleted for comment id: {comment_id}"}
        return ErrorHandler.NotFound("Comment not found")
