
from ....core.database import post_collection, user_collection
from ....models import schemas
from ...exception import ErrorHandler


class PostsHandler:

    @staticmethod
    def HandlePostCreation(request: schemas.Post):
        """
        Create a new post.
        """
        new_post = post_collection.insert_one(
            {**request.model_dump(exclude=None)})
        # Add the post details to the user db where the post is defined as well
        # user_collection.find_one_and_update(
        #     {"email": request.posted_by},
        #     {"$push": {"posts": {**request.model_dump(exclude=None)}}}
        # )
        return {"id": str(new_post.inserted_id)}

    @staticmethod
    def HandlePostReadings():
        """
        Get all the posts.
        """
        count = post_collection.count_documents({})
        if count > 0:
            users = post_collection.find()
            return users
        else:
            raise ErrorHandler.NotFound("No posts found")

    @staticmethod
    def HandlePostDeletion(post_id):
        """
        Delete a post.
        """
        post = post_collection.find_one_and_delete({"post_id": post_id})
        if post:
            return {"message": "Post deleted for post id:"+str(post_id)}
        else:
            raise ErrorHandler.NotFound("Post not found")

    @staticmethod
    def HandleUserPostsRetrieval(email):
        """
        Get all the posts of a specific user.
        """
        user = user_collection.find_one({"email": email})
        if user:
            posts = post_collection.find({"posted_by": email})
            if not posts:
                raise ErrorHandler.NotFound("No posts found for user")
            return posts
        else:
            raise ErrorHandler.NotFound("User not found")
