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
    async def HandlePostCreation(request: schemas.Post, images: Optional[List[UploadFile]]):
        """
        Create a new post.
        """
        post_data = {
            **request.model_dump(exclude=None)}
        if images:
            for image in images:
                img_id = image.filename.split(".")[0][:]
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
                return [{"id": str(post["_id"]), **post} for post in public_posts]
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
    async def HandleUserPostsRetrieval(email, user_logged_in):
        """
        Get all the posts of a specific user.
        """
        # Check if there are any posts by the user first to avoid multiple database calls
        post_count = await post_collection.count_documents({"posted_by": email})
        if post_count == 0:
            raise ErrorHandler.NotFound("No posts found for user")

        # If the requester is the user or a friend, adjust the privacy filter accordingly
        # Default to public if none of the conditions below are met
        privacy_filter = {"privacy": "public"}
        if email == user_logged_in:
            privacy_filter = {}  # No privacy filter needed if the user is retrieving their own posts
        else:
            isFriend = await user_collection.find_one({"email": user_logged_in, "friends": email})
            if isFriend:
                # Show non-private posts if the requester is a friend
                privacy_filter = {"privacy": {"$ne": "private"}}

        # Fetch posts with the determined privacy filter
        posts = await post_collection.find({"posted_by": email, **privacy_filter}).to_list(length=None)
        # Convert each post document to a dictionary and add a stringified ID
        posts_with_details = [
            {"id": str(post["_id"]), **post} for post in posts]
        return posts_with_details

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
    async def HandlePostImageUpload(post_id: str, user_logged_in: str, file: UploadFile):
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

    @staticmethod
    async def HanldePostRetrievalById(post_id: str):

        post = await post_collection.find_one({"_id": ObjectId(post_id)})
        if post:
            return post
        else:
            return ErrorHandler.NotFound("Post not found")
