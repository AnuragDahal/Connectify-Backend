from ....core.database import comments_collection, post_collection
from ....models import schemas
from .posthandler import gen_random_id
from ...exception import ErrorHandler

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
