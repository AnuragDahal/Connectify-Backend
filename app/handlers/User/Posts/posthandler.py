from app.config.cloudinary_config import uploadImage
from ....core.database import post_collection, user_collection
from ....models import schemas
from ...exception import ErrorHandler
from pymongo import ReturnDocument
import uuid
from fastapi import UploadFile
from typing import Optional


def gen_random_id():
    return str(uuid.uuid4())


class PostsHandler:
    @staticmethod
    def HandlePostCreation(request: schemas.Post, image: Optional[UploadFile]):
        """
        Create a new post.
        """
        if image:
            img_id = image.filename.split(".")[0][:10]
            img_byte = image.file.read()
            # Upload the image to the server
            img_url = uploadImage(img_id, img_byte)
        new_post = post_collection.insert_one(
            {**request.model_dump(exclude={"post_id"}), "post_id": gen_random_id(), "image": img_url})
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

    @staticmethod
    def HandlePostUpdate(request: schemas.Post, post_id: str):
        """
        Update a post.
        """
        post = post_collection.find_one_and_update(
            {"post_id": post_id},
            {"$set": {
                **request.model_dump(exclude={"post_id"}), "post_id": post_id}},
            return_document=ReturnDocument.AFTER
        )
        if post:
            return post
        raise ErrorHandler.NotFound("Post not found")

    @staticmethod
    def HandlePostImageUpload(post_id, file):
        """
        Upload an image for a post.
        """
        if not file:
            raise ErrorHandler.Error("No image found")
        post = post_collection.find_one({"post_id": post_id})
        if post:
            img_id = file.filename.split(".")[0][:10]
            img_byte = file.file.read()
            # Upload the image to the server
            img_url = uploadImage(img_id, img_byte)
            return {"image_url": img_url}
        raise ErrorHandler.NotFound("Post not found")

    @staticmethod
    def HandlePostLike(post_id, email):
        """
        Like a post.
        """
        post = post_collection.find_one({"post_id": post_id})
        if post:
            if email in post["likes"]:
                raise ErrorHandler.Error("Post already liked")
            post_collection.find_one_and_update(
                {"post_id": post_id},
                {"$addToSet": {"likes": email}}
            )
            return {"message": "Post liked"}
        return ErrorHandler.NotFound("Post not found")

    @staticmethod
    def HandleLikesCounts(post_id: str):
        """
        Get the number of likes for a post.
        """
        post = post_collection.find_one({"post_id": post_id})
        if post:
            count_likes = 0
            for like in post["likes"]:
                count_likes += 1
            return {"likes": count_likes}
        return ErrorHandler.NotFound("Post not found")
