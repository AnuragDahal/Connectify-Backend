
from ....core.database import post_collection
from ....models import schemas


class PostsHandler:

    @staticmethod
    def HandlePostCreation(request: schemas.Post):
        """
        Create a new post.
        """
        new_post = post_collection.insert_one(
            {**request.model_dump(exclude=None)})
        
        return {"id": str(new_post.inserted_id)}
