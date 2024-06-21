from ...models import schemas
from fastapi import Response, UploadFile
from ...core.database import user_collection
from ..exception import ErrorHandler
from pymongo import ReturnDocument
from ...config.cloudinary_config import uploadImage
from ...utils.passhashutils import Encrypt
from typing import Optional
from ...core.database import post_collection, comments_collection
from ...utils.passhashutils import Encrypt


class Validate:
    @staticmethod
    async def verify_email(email: str):
        check_email = await user_collection.find_one({"email": email})
        if check_email:
            return True
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
            hashed_password = Encrypt.hash_password(request.password)
            # Add the image to the server and set the url in the db
            user_data = {
                **request.model_dump(exclude={"password"}), "password": hashed_password, "isEmailVerified": False}
            if image:
                img_id = image.filename.split(".")[0][:10]
                img_byte = image.file.read()  # blocking code
                img_url = uploadImage(img_id, img_byte)  # blocking code
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
    async def update(old_email: str, new_email: str, password: str):
        """Update your email address."""

        # Check email from the cookie and the email to be updated are same
        if old_email == new_email:
            return ErrorHandler.Bad(
                "Please Enter the new email")

        # Check the password of the user
        user_details = await user_collection.find_one({"email": old_email})
        if not Encrypt.verify_password(password, user_details["password"]):
            return ErrorHandler.Unauthorized("Password is incorrect")

        # check if the new email entered is available or not
        is_available = await Validate.verify_email(new_email.email)
        if not is_available:
            user = await user_collection.find_one_and_update(
                {"email": old_email},
                {"$set": {"email": new_email.email, "isEmailVerified": False}},
                return_document=ReturnDocument.AFTER)

            if user is None:
                raise ErrorHandler.NotFound("User not found")
            return user
        else:
            return ErrorHandler.ALreadyExists("The User with the given email already exists")

    @staticmethod
    async def delete(user_email: str, res: Response):
        """
        Delete a user
        """
        # Delete the user through the email
        deleted_user = await user_collection.delete_one({"email": user_email})
        if deleted_user.deleted_count == 0:
            return ErrorHandler.NotFound("User not found")
        # Delete all the data sets associated with the user such as posts, comments, etc.
        await comments_collection.delete_many({"commented_by": user_email})
        await post_collection.delete_many({"posted_by": user_email})
        res.delete_cookie('token')
        return {"message": "User deleted successfully"}
