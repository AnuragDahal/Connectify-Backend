from ...models import schemas
from fastapi import Response, UploadFile
from ...core.database import user_collection
from ..exception import ErrorHandler
from ...config.cloudinary_config import uploadImage
from ...utils.passhashutils import Encrypt
from typing import Optional
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
    async def HandleNewUserCreation(request: schemas.UserDetails):
        """
        Insert a new user record.
        A unique `id` will be created and provided in the response.
        """
        duplicate_user = await Validate.verify_email(request.email)
        if not duplicate_user:
            hashed_password = Encrypt.hash_password(request.password)
            user_data = {
                **request.model_dump(exclude={"password"}), "password": hashed_password, "isEmailVerified": False}
            new_user = await user_collection.insert_one(user_data)
            if new_user:
                return {"message": "User created successfully"}
            return ErrorHandler.InternalServerError("User creation failed")
        return ErrorHandler.ALreadyExists("User already exists")

    @staticmethod
    async def HandleReadingUserRecords():
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
    async def HandleUserDeletion(user_email: str, password: str, res: Response):
        """
        Delete a user
        """
        # Check the password is correct
        user_details = await user_collection.find_one({"email": user_email})
        if not Encrypt.verify_password(password, user_details["password"]):
            return ErrorHandler.Unauthorized("Incorrect Password")

        # Delete the user through the email
        deleted_user = await user_collection.delete_one({"email": user_email})
        if deleted_user.deleted_count == 0:
            return ErrorHandler.NotFound("User not found")
        # Delete all the data sets associated with the user such as bills etc
        res.delete_cookie('token')
        return {"message": "User deleted successfully"}
