from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from enum import Enum
from bson import ObjectId


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
    isEmailVerified: Optional[bool] = False
    profile_picture: Optional[str] = []


class UserDetails(BaseModel):
    name: str
    email: str
    password: str
    isEmailVerified: Optional[bool] = False
    profile_picture: Optional[str] = []
    user_plan: Optional[str] = "free"
