from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request, UploadFile
from ..handlers.User.Posts.posthandler import PostsHandler
from ..handlers import ErrorHandler


class ImageUploadMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/api/v1/posts/create" and request.method == "POST":
            form = await request.form()
            image: UploadFile = form.get("image")
            if image:
                post_id = form.get("post_id")
                if not post_id:
                    return JSONResponse(status_code=400, content={"message": "Post ID not found"})

                try:
                    img_url = PostsHandler.HandlePostImageUpload(
                        post_id, image)
                    form = dict(form)
                    form["image"] = img_url["image_url"]
                    request._form = form
                except ErrorHandler.Error as e:
                    return JSONResponse(status_code=400, content={"message": str(e)})
                except ErrorHandler.NotFound as e:
                    return JSONResponse(status_code=404, content={"message": str(e)})

        response = await call_next(request)
        return response
