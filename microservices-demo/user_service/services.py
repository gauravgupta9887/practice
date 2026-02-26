import uuid
from sqlalchemy.orm import Session
from .models import User
from .schemas import RegisterRequest, LoginRequest, UserResponse
from .shared.logger import logger
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, data: RegisterRequest) -> UserResponse:
        if self.db.query(User).filter(User.email == data.email).first():
            raise ValueError("Email already in use")
        user = User(email=data.email,
                    password_hash=hash_password(data.password))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        logger.info(f"User {user.id} registered")
        return UserResponse.from_orm(user)

    def authenticate(self, data: LoginRequest) -> str:
        user = self.db.query(User).filter(User.email == data.email).first()
        if not user or not verify_password(data.password, user.password_hash):
            raise ValueError("Invalid credentials")
        from flask_jwt_extended import create_access_token
        access_token = create_access_token(identity=user.id)
        logger.info(f"User {user.id} logged in")
        return access_token