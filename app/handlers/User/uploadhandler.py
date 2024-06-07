from ...config.cloudinary_config import uploadImage
from ...core.database import user_collection
from pymongo import ReturnDocument
from .userhandler import Validate
from ..exception import ErrorHandler


class UploadManager:
    @staticmethod
    def HandleUploadProfilePic(user_email, img):
        """
        Upload the user profile picture.
        """
        # Check the user in db
        try:
            isUser = Validate.verify_email(user_email)
            if not isUser:
                return ErrorHandler.NotFound("User not found")
            filename = img.filename.split(".")[0][:10]
            img_bytes = img.file.read()
            # Upload the image and get its URL
            img_url = uploadImage(filename, img_bytes)
            # Save the image URL in the database
            user = user_collection.find_one_and_update(
                {"email": user_email},
                {"$set": {"profile_pic": img_url}},
                # this will return the updated document
                return_document=ReturnDocument.AFTER
            )
            return user
        except Exception as e:
            return ErrorHandler.Error(e)
