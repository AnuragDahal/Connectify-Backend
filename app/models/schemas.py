from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from bson import ObjectId


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
    post_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = None
    content: Optional[str] = None
    posted_by: Optional[str] = None
    posted_on: datetime = datetime.now(timezone.utc)
    image: Optional[str] = None


class UserDetails(BaseModel):
    name: str
    email: str
    isEmailVerified: Optional[bool]
    friends: Optional[List[str]] = []
    profile_picture: Optional[str] = str()
    # posts: Optional[List[Dict[str, Any]]] = []
    posts: Optional[List[str]] = []
    commented: Optional[List[str]] = []
    comments_on_posts: Optional[List[str]] = []


class UpdateUserEmail(BaseModel):
    email: str
