from ....core.database import comments_collection, post_collection, user_collection
from ....models import schemas
from pymongo import ReturnDocument
from ...exception import ErrorHandler
from bson import ObjectId


class CommentsHandler:

    @staticmethod
    async def HandleCommentCreation(request: schemas.Comments, email):
        """
        Create a comment.
        """
        # Check the use creating the comment is the logged in user or not
        if request.commented_by != email:
            return ErrorHandler.Unauthorized("You are not authorized to comment on this post")
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
            {"$addToSet": {"comments_on_posts": request.post_id}}
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
    async def HandleCommentUpdate(request: schemas.Comments, comment_id: str, email_from_header: str):
        """Update the existing comment"""
        # Check the user updating the comment is the logged in user or not
        if request.commented_by != email_from_header:
            return ErrorHandler.Unauthorized("You are not authorized to update this comment")
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
    async def HandlePostCommentDeletion(comment_id: str, email_from_header: str):
        """
        Delete a comment.
        """
        # check if the user deleting the comment owns the post or not
        comment = await comments_collection.find_one({"_id": ObjectId(comment_id)})
        user = await user_collection.find_one({"email": email_from_header})
        if comment:
            if comment["post_id"] in user["posts"]:
                await post_collection.find_one_and_update(
                    {"comments": comment_id},
                    {"$pull": {"comments": comment_id}}
                )

                await comments_collection.find_one_and_delete({"_id": ObjectId(comment_id)})
                # Also remove the comment from the user's commented list
                await user_collection.find_one_and_update(
                    {"email": comment["commented_by"]},
                    {"$pull": {"commented": comment_id}})
                # Check for the count of the comments in the post and remove the post from the user's comments_on_posts list if the comment count reaches 0

                count_documents = await comments_collection.count_documents({"post_id": comment["post_id"]})
                if count_documents == 0:
                    await user_collection.find_one_and_update(
                        {"email": comment["commented_by"]},
                        {"$pull": {"comments_on_posts": comment["post_id"]}}
                    )
                return {"message": f"Comment deleted for comment id: {comment_id}"}
            else:
                return ErrorHandler.Unauthorized("You are not authorized to delete this comment")
        else:
            return ErrorHandler.NotFound("Comment not found")

    @staticmethod
    async def HandleOwnCommentDeletion(comment_id: id, user_logged_in: str):
        # Check if the user deleting the comment is the owner of the comment
        comment = await comments_collection.find_one({"_id": ObjectId(comment_id)})
        if comment:
            if comment["commented_by"] == user_logged_in:
                # Remove the comment from the comments collection
                await comments_collection.find_one_and_delete({"_id": ObjectId(comment_id)})
                # Also remove the comment from the user's commented list
                await user_collection.find_one_and_update(
                    {"email": user_logged_in},
                    {"$pull": {"commented": comment_id}})
                # Also remove the comment from the post comments list
                await post_collection.find_one_and_update(
                    {"_id": comment["post_id"]},
                    {"$pull": {"comments": comment_id}}
                )
                # Check for the count of the comments in the post and remove the post from the user's comments_on_posts list if the comment count reaches 0
                count_documents = await comments_collection.count_documents({"post_id": comment["post_id"]})
                if count_documents == 0:
                    await user_collection.find_one_and_update(
                        {"email": user_logged_in},
                        {"$pull": {"comments_on_posts": comment["post_id"]}}
                    )
                return {"message": f"Comment deleted for comment id: {comment_id}"}
            return ErrorHandler.Unauthorized("You are not authorized to delete this comment")
        return ErrorHandler.NotFound("Comment not found")
