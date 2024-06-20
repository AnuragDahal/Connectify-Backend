from app.config.cloudinary_config import uploadImage
from ....core.database import post_collection, user_collection, comments_collection
from ....models import schemas
from ...exception import ErrorHandler
from pymongo import ReturnDocument
from ...Auth.authhandler import Validate
import uuid
from fastapi import UploadFile
from typing import Optional, List
from bson import ObjectId
from datetime import datetime, timezone


def gen_random_id():
    return str(uuid.uuid4())


class PostsHandler:
    @staticmethod
    async def HandlePostCreation(request: schemas.Post, user_logged_in: str, images: Optional[List[UploadFile]]):
        """
        Create a new post.
        """
        if request.posted_by != user_logged_in:
            return ErrorHandler.Unauthorized("You are not authorized to create a post for another user")
        post_data = {
            **request.model_dump(exclude=None)}
        if images:
            for image in images:
                img_id = image.filename.split(".")[0][:10]
                img_byte = await image.read()
                # Upload the image to the server
                img_url = uploadImage(img_id, img_byte)
                image_list = post_data["images"]
                image_list.append(img_url)
        new_post = await post_collection.insert_one(post_data)
        await user_collection.update_one({"email": request.posted_by},
                                         {"$addToSet": {"posts": str(new_post.inserted_id)}})
        return {"id": str(new_post.inserted_id)}

    @staticmethod
    async def HandlePublicPostReadings():
        """
        Get all the public posts.
        """
        documents = await post_collection.find({}).to_list(length=None)
        if documents:
            public_posts = [
                document for document in documents if document["privacy"] == "public"]
            if public_posts:
                return public_posts
            return ErrorHandler.NotFound("No public posts found")
        return ErrorHandler.NotFound("No posts found")

    @staticmethod
    async def HandlePostDeletion(post_id, user_logged_in: str):
        """
        Delete a post.
        """
        user = await user_collection.find_one({"email": user_logged_in})
        if post_id not in user["posts"]:
            return ErrorHandler.Unauthorized("You are not authorized to delete this post")
        post = await post_collection.find_one({"_id": ObjectId(post_id)})
        if post:
            # Delete all the comments for the post and then delete the post
            await comments_collection.delete_many({"post_id": ObjectId(post_id)})
            await post_collection.delete_one({"_id": ObjectId(post_id)})
            return {"message": "Post and comments deleted for post id:"+str(post_id)}
        else:
            raise ErrorHandler.NotFound("Post not found")

    @staticmethod
    async def HandleUserPostsRetrieval(email):
        """
        Get all the posts of a specific user.
        """
        if await Validate.verify_email(email):
            post_count = await post_collection.count_documents({"posted_by": email})
            if post_count == 0:
                raise ErrorHandler.NotFound("No posts found for user")
            else:
                posts_cursor = post_collection.find({"posted_by": email})
                posts = await posts_cursor.to_list(length=None)
                return posts
        else:
            raise ErrorHandler.NotFound("User not found")

    @staticmethod
    async def HandlePostUpdate(request: schemas.PostUpdate, user_logged_in: str, post_id: str, images: Optional[List[UploadFile]]):
        """
        Update a post.
        """
        # Check if the user is authorized to update the post
        user = await user_collection.find_one({"email": user_logged_in})
        if post_id not in user["posts"]:
            return ErrorHandler.Unauthorized("You are not authorized to update this post")
        # Fetch the existing post
        existing_post = await post_collection.find_one({"_id": ObjectId(post_id)})

        # Initialize images
        images_list = existing_post["images"] if not images else []

        # Update the post with the new data
        post_data = {
            "title": request.title if request.title else existing_post["title"],
            "content": request.content if request.content else existing_post["content"],
            "images": images_list,
            "posted_on": datetime.now(timezone.utc),
        }
        if images:
            for image in images:
                img_id = image.filename.split(".")[0][:10]
                img_byte = await image.read()
                # Upload the image to the server
                img_url = uploadImage(img_id, img_byte)
                post_data["images"].append(img_url)
        updated_post = await post_collection.find_one_and_update(
            {"_id": ObjectId(post_id)}, {"$set": post_data}, return_document=ReturnDocument.AFTER)
        return updated_post

    @staticmethod
    async def HandlePostImageUpload(post_id: str, user_logged_in: str, file):
        """
        Upload an image for a post.
        """
        try:
            user = await user_collection.find_one({"email": user_logged_in})
            if post_id not in user["posts"]:
                return ErrorHandler.Unauthorized("You are not authorized to upload image to this post")
            if not file:
                raise ErrorHandler.Error("No image found")
            post = await post_collection.find_one({"_id": ObjectId(post_id)})
            if post:
                img_id = file.filename.split(".")[0][:10]
                img_byte = await file.read()
                # Upload the image to the server
                img_url = uploadImage(img_id, img_byte)
                # Put the image in the document of the post
                await post_collection.find_one_and_update(
                    {"_id": ObjectId(post_id)},
                    {"$set": {"image": img_url}}
                )
                return {"image_url": img_url}
            raise ErrorHandler.NotFound("Post not found")
        except Exception as e:
            raise ErrorHandler.Error(str(e))

    @staticmethod
    async def HandlePostLike(post_id, email):
        """
        Like a post.
        """
        # Check if the user req to like post exists or not
        if Validate.verify_email(email):
            post = await post_collection.find_one({"_id": ObjectId(post_id)})
            if post:
                # If the user has liked the post already then remove the like from the post
                if email in post["likes"]:
                    await post_collection.update_one({"_id": ObjectId(post_id)},
                                                     {"$pull": {"likes": email}})
                    return {"message": "Post unliked"}
                # use update_one if no return is needed and use find_one_and_update if return is needed
                await post_collection.update_one(
                    {"_id": ObjectId(post_id)},
                    {"$addToSet": {"likes": email}}
                )
                return {"message": "Post liked"}
            return ErrorHandler.NotFound("Post not found")
        return ErrorHandler.NotFound(f"User with email {email} not found in the database")

    @staticmethod
    async def HandleLikesCounts(post_id: str):
        """
        Get the number of likes for a post.
        """
        post = await post_collection.find_one({"_id": ObjectId(post_id)})
        if post:
            count_likes = len(post["likes"])
            return {"likes": count_likes}
        return ErrorHandler.NotFound("Post not found")

    @staticmethod
    async def HandleFriendPostsRetrieval(friend_email: str, user_logged_in: str):
        """
        Get all the public posts and friend_posts.
        """
        user = await user_collection.find_one({"email": user_logged_in})
        if not user:
            return ErrorHandler.NotFound("No user found")
        if friend_email in user["friends"]:
            post_count = await post_collection.count_documents({"posted_by": friend_email})
            if post_count == 0:
                raise ErrorHandler.NotFound("No posts found for user")
            else:
                posts_cursor = post_collection.find(
                    {"posted_by": friend_email})
                posts = await posts_cursor.to_list(length=None)
                available_post = [
                    post for post in posts if post["privacy"] != "private"]
                return available_post
        else:
            return ErrorHandler.NotFound("No friends found ")

    @staticmethod
    async def HandlePostPrivacyUpdate(post_id: str, privacy: str, user_logged_in: str):
        """Change the privacy of your posts to public, friends or private."""
        user = await user_collection.find_one({"email": user_logged_in})
        if post_id not in user["posts"]:
            return ErrorHandler.Unauthorized("You are not authorized to update this post")
        post = await post_collection.find_one({"_id": ObjectId(post_id)})
        if post is not None:
            if privacy not in ["public", "friends", "private"]:
                return ErrorHandler.Error("Invalid privacy type")
            post_privacy = await post_collection.find_one_and_update(
                {"_id": ObjectId(post_id)},
                {"$set": {"privacy": privacy}}, return_document=ReturnDocument.AFTER)
            return {"message": "Post privacy updated to "+privacy}
        else:
            return ErrorHandler.NotFound("Post not found")
