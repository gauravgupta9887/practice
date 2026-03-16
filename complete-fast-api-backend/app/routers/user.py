from app.database import get_db
from app.models import Users
from app.schemas import UserCreate, UserOut
from app.utils import hashed_pwd
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # hash the password
    hashed_password = hashed_pwd(user.password)
    user.password = hashed_password
    new_user = Users(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with same email exists: {e}",
        )
    # this block is not getting executed anymore
    return new_user


@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id).first()

    if not user:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User \
                      with id:{id} not found")

    return user
