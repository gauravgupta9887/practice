from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int]


class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        orm_mode = True
