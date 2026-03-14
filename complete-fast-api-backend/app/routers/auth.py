from fastapi import APIRouter, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Users
from app.utils import verify
from app.oauth2 import create_access_token
from app.schemas import Token

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    # username, password
    # {
    #     "username":"",
    #     "password":""
    # }
    user = db.query(Users).filter(Users.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    # create a token
    access_token = create_access_token(data={"user_id": user.id})
    # return the token
    return {"access_token": access_token, "token_type": "bearer"}
