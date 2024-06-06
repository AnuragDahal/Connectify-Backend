from pydantic import BaseModel, EmailStr
from typing import List, Optional


class User(BaseModel):
    name: str
    email: str
    password: str
    isEmailVerified: Optional[bool]
    friends: Optional[List[str]]
    profile_picture: Optional[str]
    posts: Optional[List[str]]
    commented: Optional[List[str]]
    comments_on_posts: Optional[List[str]]


class OauthUser(BaseModel):
    name: str
    email: str
    isEmailVerified: Optional[bool]
    friends: Optional[List[str]]
    profile_picture: Optional[str]
    posts: Optional[List[str]]
    commented: Optional[List[str]]
    comments_on_posts: Optional[List[str]]


class UpdateUserEmail(BaseModel):
    email: str


class StoreOtp(BaseModel):
    email: EmailStr
    otp: str
    expires_on: str
