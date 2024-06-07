from ...config.cloudinary_config import uploadImage
from ...core.database import user_collection
from pymongo import ReturnDocument


class UploadManager:
    @staticmethod
    def HandleUploadProfilePic(user_email, img):
        """
        Upload the user profile picture.
        """
        filename = img.filename.split(".")[0][:10]
        img_bytes = img.file.read()
        # Upload the image and get its URL
        img_url = uploadImage(filename, img_bytes)
        # Save the image URL in the database
        user = user_collection.find_one_and_update(
            {"email": user_email},
            {"$set": {"profile_pic": img_url}},
            return_document=ReturnDocument.AFTER
        )
        print(user)
