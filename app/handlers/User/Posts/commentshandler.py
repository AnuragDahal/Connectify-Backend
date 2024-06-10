from ....core.database import comments_collection, post_collection
from ....models import schemas
from .posthandler import gen_random_id


class CommentsHandler:

    @staticmethod
    def HandleCommentCreation(request: schemas.Comments):
        """
        Create a comment.
        """
        new_comment = comments_collection.insert_one(
            {**request.model_dump(exclude=None)})
        # Add the comment_id to the post_id in the posts collection
        comment_id = str(new_comment.inserted_id)
        post_collection.find_one_and_update({
            "post_id": request.post_id},
            {"$addToSet": {'comments': comment_id}}

        )
        return {"id": str(new_comment.inserted_id)}
