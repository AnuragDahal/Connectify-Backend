from ...models import schemas
from fastapi import Request, Response, UploadFile
from ...core.database import user_collection
from ..exception import ErrorHandler
from pymongo import ReturnDocument
from ...config.dependencies import verify_token
from ...config.cloudinary_config import uploadImage
from ...utils.passhashutils import Encryptor
from typing import Optional
from ...core.database import post_collection, comments_collection


class Validate:
    @staticmethod
    async def verify_email(email: str):
        check_email = await user_collection.find_one({"email": email})
        if check_email:
            return email
        return False


class UserManager:
    @staticmethod
    async def create(request: schemas.UserDetails, image: Optional[UploadFile]):
        """
        Insert a new user record.
        A unique `id` will be created and provided in the response.
        """
        duplicate_user = await Validate.verify_email(request.email)
        if not duplicate_user:
            hashed_password = Encryptor.hash_password(request.password)
            # Add the image to the server and set the url in the db
            user_data = {
                **request.model_dump(exclude={"password"}), "password": hashed_password, "isEmailVerified": False}
            if image:
                img_id = image.filename.split(".")[0][:10]
                img_byte = await image.file.read()  # blocking code
                img_url = await uploadImage(img_id, img_byte)  # blocking code
                user_data["image"] = img_url
                # Add the img url to the user's db
            new_user = await user_collection.insert_one(user_data)
            return {"id": str(new_user.inserted_id)}
        return ErrorHandler.ALreadyExists("User already exists")

    @staticmethod
    async def read():
        """
        Retrieve all user records.
        """
        count = await user_collection.count_documents({})
        if count > 0:
            # this is a asynchronous cursor so we need to iterate over it using async for loop
            AsyncIOMotorCursor = user_collection.find()
            users = []
            async for user in AsyncIOMotorCursor:
                users.append(user)
            return users
        else:
            raise ErrorHandler.NotFound("No user found")

    @staticmethod
    async def update(old_email: str, request: Request, new_email: schemas.UpdateUserEmail):
        """"""
        # Get the user email from the cookie
        logged_in_user_email = await verify_token(request)
        # Check email from the cookie and the email to be updated are same
        if old_email != logged_in_user_email:
            raise ErrorHandler.Forbidden(
                "You are not authorized to perform this action")
            # check if the new email entered is available or not
        is_available = await Validate.verify_email(new_email.email)
        if not is_available:
            user = await user_collection.find_one_and_update(
                {"email": logged_in_user_email},
                {"$set": {"email": new_email.email}},
                return_document=ReturnDocument.AFTER
            )
            if user is None:
                raise ErrorHandler.NotFound("User not found")
            return user
        else:
            return ErrorHandler.Error("Bad request")

    @staticmethod
    async def delete(request: Request, res: Response):
        """
        Delete a user
        """
        # Get the user email from the cookie
        user_email = await verify_token(request)
        # Delete the user through the email
        deleted_user = await user_collection.delete_one({"email": user_email})
        # Delete all the data sets associated with the user such as posts, comments, etc.
        await comments_collection.delete_many({"commented_by": user_email})
        await post_collection.delete_many({"posted_by": user_email})
        res.delete_cookie('token')
        if deleted_user.deleted_count == 0:
            raise ErrorHandler.NotFound("User not found")
        return {"message": "User deleted successfully"}
