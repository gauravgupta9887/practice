from .shared.schemas.base import BaseRequest, BaseResponse
from pydantic import EmailStr

class RegisterRequest(BaseRequest):
    email: EmailStr
    password: str

class LoginRequest(BaseRequest):
    email: EmailStr
    password: str

class UserResponse(BaseResponse):
    id: int
    email: EmailStr
    balance: float