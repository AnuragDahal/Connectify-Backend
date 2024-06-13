from app.config.cloudinary_config import uploadImage
from ....core.database import post_collection, user_collection, comments_collection
from ....models import schemas
from ...exception import ErrorHandler
from pymongo import ReturnDocument
from ...Auth.authhandler import Validate
import uuid
from fastapi import UploadFile
from typing import Optional
from bson import ObjectId


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
            save_post = post_collection.insert_one(
                {**request.model_dump(exclude=None), "image": img_url, "privacy": "public"})
        new_post = post_collection.insert_one(
            {**request.model_dump(exclude=None), "privacy": "public"})
        return {"id": str(new_post.inserted_id)}

    @staticmethod
    def HandlePublicPostReadings():
        """
        Get all the public posts.
        """
        documents = list(post_collection.find({}))
        if documents:
            public_posts = [
                document for document in documents if document["privacy"] == "public"]
            if public_posts:
                return public_posts
            return ErrorHandler.NotFound("No public posts found")
        return ErrorHandler.NotFound("No posts found")

    @staticmethod
    def HandlePostDeletion(post_id):
        """
        Delete a post.
        """
        post = post_collection.find_one({"_id": ObjectId(post_id)})
        if post:
            # Delete all the comments for the post and then delete the post
            comments_collection.delete_many({"post_id": ObjectId(post_id)})
            post_collection.delete_one({"_id": ObjectId(post_id)})
            return {"message": "Post and comments deleted for post id:"+str(post_id)}
        else:
            raise ErrorHandler.NotFound("Post not found")

    @staticmethod
    def HandleUserPostsRetrieval(email):
        """
        Get all the posts of a specific user.
        """
        if Validate.verify_email(email):
            post_count = post_collection.count_documents({"posted_by": email})
            if post_count == 0:
                raise ErrorHandler.NotFound("No posts found for user")
            else:
                posts_cursor = post_collection.find({"posted_by": email})
                return posts_cursor
        else:
            raise ErrorHandler.NotFound("User not found")

    @staticmethod
    def HandlePostUpdate(request: schemas.Post, post_id: str):
        """
        Update a post.
        """
        post = post_collection.find_one_and_update(
            {"_id": ObjectId(post_id)},
            {"$set": {
                **request.model_dump(exclude=None), "_id": ObjectId(post_id)}},
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
        try:
            if not file:
                raise ErrorHandler.Error("No image found")
            post = post_collection.find_one({"_id": ObjectId(post_id)})
            if post:
                img_id = file.filename.split(".")[0][:10]
                img_byte = file.file.read()
                # Upload the image to the server
                img_url = uploadImage(img_id, img_byte)
                # Put the image in the document of the post
                post_collection.find_one_and_update(
                    {"_id": ObjectId(post_id)},
                    {"$set": {"image": img_url}}
                )
                return {"image_url": img_url}
            raise ErrorHandler.NotFound("Post not found")
        except Exception as e:
            raise ErrorHandler.Error(str(e))

    @staticmethod
    def HandlePostLike(post_id, email):
        """
        Like a post.
        """
        # Check if the user req to like post exists or not
        if Validate.verify_email(email):
            post = post_collection.find_one({"_id": ObjectId(post_id)})
            if post:
                # If the user has liked the post already then remove the like from the post
                if email in post["likes"]:
                    post_collection.update_one({"_id": ObjectId(post_id)},
                                               {"$pull": {"likes": email}})
                    return {"message": "Post unliked"}
                # use update_one if no return is needed and use find_one_and_update if return is needed
                post_collection.update_one(
                    {"_id": ObjectId(post_id)},
                    {"$addToSet": {"likes": email}}
                )
                return {"message": "Post liked"}
            return ErrorHandler.NotFound("Post not found")
        return ErrorHandler.NotFound(f"User with email {email} not found in the database")

    @staticmethod
    def HandleLikesCounts(post_id: str):
        """
        Get the number of likes for a post.
        """
        post = post_collection.find_one({"_id": ObjectId(post_id)})
        if post:
            count_likes = 0
            for like in post["likes"]:
                count_likes += 1
            return {"likes": count_likes}
        return ErrorHandler.NotFound("Post not found")

    @staticmethod
    def HandleFriendPostsRetrieval(user_email: str):
        """
        Get all the public posts.
        """
        documents = list(post_collection.find({}))
        print(type(documents))
        if documents:
            friends_posts = [document for document in documents if
                             (document["privacy"] == "friends" and user_email in document["friends"])]
            if friends_posts:
                return friends_posts
            return ErrorHandler.NotFound("No posts found for friends")
        return ErrorHandler.NotFound("No posts found")

    @staticmethod
    def HandlePostPrivacyUpdate(post_id: str, privacy: str):
        """Change the privacy of your posts to public, friends or private."""
        post = post_collection.find_one({"_id": ObjectId(post_id)})
        if post is not None:
            if privacy not in ["public", "friends", "private"]:
                return ErrorHandler.Error("Invalid privacy type")
            post_privacy = post_collection.find_one_and_update(
                {"_id": ObjectId(post_id)},
                {"$set": {"privacy": privacy}}, return_document=ReturnDocument.AFTER)
            return {"message": "Post privacy updated to "+privacy}
            # return post_privacy
        else:
            return ErrorHandler.NotFound("Post not found")
