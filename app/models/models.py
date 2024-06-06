from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from fastapi import UploadFile


class User(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    isEmailVerified: Optional[bool] = Field(default=False)
    friends: Optional[List[str]] = Field(None, min_items=0, max_items=1000)
    profile_picture: Optional[str] = Field(None)
    posts: Optional[List[str]] = Field(None, min_items=0)
    commented: Optional[List[str]] = Field(None, min_items=0)
    comments_on_posts: Optional[List[str]] = Field(None, min_items=0)


class OauthUser(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., min_length=5, max_length=100)
    isEmailVerified: Optional[bool] = Field(default=False)
    profile_picture: Optional[str] = Field(None)
    posts: Optional[List[str]] = Field(None, min_items=0)
    commented: Optional[List[str]] = Field(None, min_items=0)
    comments_on_posts: Optional[List[str]] = Field(None, min_items=0)
    friends: Optional[List[str]] = Field(None, min_items=0, max_items=1000)
