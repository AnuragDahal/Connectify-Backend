from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone


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


class Post(BaseModel):
    title: str
    content: str
    posted_by: str
    posted_on: datetime = datetime.now(timezone.utc)
    image: str = None


class UserDetails(BaseModel):
    name: str
    email: str
    isEmailVerified: Optional[bool]
    friends: Optional[List[str]] = []
    profile_picture: Optional[str] = str()
    # posts: Optional[List[Dict[str, Any]]] = []
    postsL: Optional[List[str]] = []
    commented: Optional[List[str]] = []
    comments_on_posts: Optional[List[str]] = []


class UpdateUserEmail(BaseModel):
    email: str
