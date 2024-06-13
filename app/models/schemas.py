from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from enum import Enum


class Privacy(str, Enum):
    public = "public"
    private = "private"
    friends = "friends"


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


class Comments(BaseModel):
    post_id: str
    comment: str
    commented_by: str = None
    commented_on: datetime = datetime.now(timezone.utc)


class Post(BaseModel):
    title: str
    content: str = None
    posted_by: str = None
    posted_on: datetime = datetime.now(timezone.utc)
    images: Optional[List[str]] = []
    likes: Optional[List[str]] = []
    comments: Optional[List[str]] = []
    privacy: Privacy = Privacy.public.value


class UserDetails(BaseModel):
    name: str
    email: str
    password: str
    isEmailVerified: Optional[bool] = False
    friends: Optional[List[str]] = []
    friend_requests: Optional[List[str]] = []
    profile_picture: Optional[str] = str()
    # posts: Optional[List[Dict[str, Any]]] = []
    posts: Optional[List[str]] = []
    commented: Optional[List[str]] = []
    comments_on_posts: Optional[List[str]] = []


class UpdateUserEmail(BaseModel):
    email: str
