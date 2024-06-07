from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import UploadFile, File


class UserSignUp(BaseModel):
    name: str
    email: str
    password: str


class OauthUser(BaseModel):
    name: str
    email: str
    isEmailVerified: Optional[bool]
    isEmailVerified: Optional[bool] = False
    friends: Optional[List[str]] = []
    profile_picture: Optional[str] = []
    posts: Optional[List[str]] = []
    commented: Optional[List[str]] = []
    comments_on_posts: Optional[List[str]] = []


class UserDetails(BaseModel):
    name: str
    email: str
    isEmailVerified: Optional[bool]
    friends: Optional[List[str]] = []
    profile_picture: Optional[str] = str()
    posts: Optional[List[str]] = []
    commented: Optional[List[str]] = []
    comments_on_posts: Optional[List[str]] = []


class UpdateUserEmail(BaseModel):
    email: str


class Post(BaseModel):
    title: str
    content: str
    posted_by: str
    posted_on: datetime = datetime.now(timezone.utc)
    image: str = None
