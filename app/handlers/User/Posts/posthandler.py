from fastapi import Request
from ....core.database import user_collection


class PostsHandler:

    @staticmethod
    def HandlePostCreation(request: Request):
        """
        Create a new post.
        """
        new_post = user_collection.insert_one(
            {**request.model_dump(exclude=None)})
        return {"id": str(new_post.inserted_id)}
