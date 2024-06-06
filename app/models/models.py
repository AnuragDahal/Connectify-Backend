from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
# from fastapi import UploadFile
from datetime import datetime, timezone


class User(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    isEmailVerified: Optional[bool] = Field(default_factory=lambda: False)
    friends: Optional[List[str]] = Field(
        default_factory=lambda: None, min_items=0, max_items=1000)
    profile_picture: Optional[str] = Field(
        default_factory=lambda: None, min_length=0, max_length=1000)
    posts: Optional[List[str]] = Field(
        default_factory=lambda: None, min_items=0)
    commented: Optional[List[str]] = Field(
        default_factory=lambda: None, min_items=0)
    comments_on_posts: Optional[List[str]] = Field(
        default_factory=lambda: None, min_items=0)


class OauthUser(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., min_length=5, max_length=100)
    isEmailVerified: Optional[bool] = Field(default_factory=lambda: True)
    profile_picture: Optional[str] = Field(None)
    posts: Optional[List[str]] = Field(None, min_items=0)
    commented: Optional[List[str]] = Field(None, min_items=0)
    comments_on_posts: Optional[List[str]] = Field(None, min_items=0)
    friends: Optional[List[str]] = Field(None, min_items=0, max_items=1000)


class Otp(BaseModel):
    email: EmailStr = Field(..., min_length=5, max_length=100)
    otp: str = Field(..., min_length=6, max_length=6)
    expires_on: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
