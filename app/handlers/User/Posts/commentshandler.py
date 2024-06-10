from ....core.database import comments_collection, post_collection
from ....models import schemas
from pymongo import ReturnDocument
from ...exception import ErrorHandler
from bson import ObjectId


class CommentsHandler:

    @staticmethod
    def HandleCommentCreation(request: schemas.Comments):
        """
        Create a comment.
        """

        if not post_collection.find_one({"post_id": request.post_id}):
            return ErrorHandler.NotFound("Post not found")
        new_comment = comments_collection.insert_one(
            {**request.model_dump(exclude=None)})
        # Add the comment_id to the post_id in the posts collection
        comment_id = str(new_comment.inserted_id)
        post_collection.find_one_and_update({
            "post_id": request.post_id},
            {"$addToSet": {'comments': comment_id}}
        )

        return {"id": str(new_comment.inserted_id)}

    @staticmethod
    def HandleCommentReadings():
        """
        Get all the comments.
        """
        comments_count = comments_collection.count_documents({})
        if comments_count > 0:
            comments = comments_collection.find()
            return comments
        return ErrorHandler.NotFound("No comments found")

    @staticmethod
    def HandleCommentUpdate(request: schemas.Comments, comment_id: str):
        '''Update the existing comment'''
        # Check if the post exists or not
        is_post = post_collection.find_one({"post_id": request.post_id})
        if is_post:
            updated_comment = comments_collection.find_one_and_update(
                {"_id": ObjectId(comment_id)},
                {"$set": request.model_dump(exclude={"comment_id"})},
                return_document=ReturnDocument.AFTER
            )
            if updated_comment:
                return updated_comment
            return ErrorHandler.NotFound("Failed to update comment")
        return ErrorHandler.NotFound("Post not found")

    @staticmethod
    def HandleCommentDeletion(comment_id: str):
        """
        Delete a comment.
        """
        is_comment = comments_collection.find_one(
            {"_id": ObjectId(comment_id)})
        if is_comment:
            # Remove the comment_id from the post_id in the posts collection
            post_collection.find_one_and_delete(
                {"comments": comment_id}
            )
            # Delete the comment from the comments_collection
            delete_comment = comments_collection.find_one_and_delete(
                {"_id": ObjectId(comment_id)})
            return {"message": "Comment deleted for comment id:"+str(comment_id)}
        return ErrorHandler.NotFound("Comment not found")
