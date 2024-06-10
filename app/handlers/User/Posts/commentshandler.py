from ....core.database import comments_collection
from ....models import schemas
from .posthandler import gen_random_id


class CommentsHandler:

    @staticmethod
    def HandleCommentCreation(request: schemas.Comments):
        """
        Create a comment.
        """
        new_comment = comments_collection.insert_one(
            {**request.model_dump(exclude={"comment_id"}), "comment_id": gen_random_id()})
        return {"id": str(new_comment.inserted_id)}
