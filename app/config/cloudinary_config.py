
# Set your Cloudinary credentials
# ==============================
import json
import cloudinary.api
import cloudinary.uploader
from cloudinary import CloudinaryImage
import cloudinary
from dotenv import load_dotenv
load_dotenv()


config = cloudinary.config(secure=True)


# print("****1. Set up and configure the SDK:****\nCredentials: ",
#       config.cloud_name, config.api_key, "\n")


def uploadImage(img_id, img_path):

    # Upload the image and get its URL
    # ==============================

    # Upload the image.
    # Set the asset's public ID and allow overwriting the asset with new versions
    cloudinary.uploader.upload(img_path,
                               public_id=img_id, unique_filename=False, overwrite=True)

    # Build the URL for the image and save it in the variable 'srcURL'
    srcURL = CloudinaryImage(img_id).build_url()

    # Copy this URL in a browser tab to generate the image on the fly.
    print("****2. Upload the image and get its URL****\nImage URL: ", srcURL, "\n")


def getAssetInfo(public_id):

    # Get and use details of the image
    # ==============================

    # Get image details and save it in the variable 'image_info'.
    image_info = cloudinary.api.resource(public_id)
    # print("****3. Get and use details of the image****\nUpload response:\n",
    json.dumps(image_info, indent=2)

    # Assign tags to the uploaded image based on its width. Save the response to the update in the variable 'update_resp'.
    if image_info["width"] > 900:
        update_resp = cloudinary.api.update(
            f"{public_id}", tags="large")
    elif image_info["width"] > 500:
        update_resp = cloudinary.api.update(
            f"{public_id}", tags="medium")
    else:
        update_resp = cloudinary.api.update(
            f"{public_id}", tags="small")

    # Log the new tag to the console.
    print("New tag: ", update_resp["tags"], "\n")


def createTransformation(public_id):

    # Transform the image
    # ==============================

    transformedURL = CloudinaryImage(public_id).build_url(
        width=100, height=150, crop="fill")

    # Log the URL to the console
    print("****4. Transform the image****\nTransfrmation URL: ", transformedURL, "\n")




