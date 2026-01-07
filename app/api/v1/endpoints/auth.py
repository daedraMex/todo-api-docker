from fastapi import APIRouter
from datetime import timedelta
from fastapi import APIRouter,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from app.core import security
from app.core.database import get_db
from app.repositories.user_repository import user_repository
from app.schemas import auth as auth_schemas


router = APIRouter()

@router.post("/register", response_model=auth_schemas.UserPublic, status_code=status.HTTP_201_CREATED)
def register(
    user_in: auth_schemas.UserCreate,
    db: Session = Depends(get_db),
    ) -> Any:
    if user_repository.get_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    if user_repository.get_by_username(db, username=user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )
    hashed_password = security.get_password_hash(user_in.password)
    return user_repository.create_user(
        db,
        obj_in=user_in,
        hashed_password=hashed_password,
    )
@router.post("/login/access-token", response_model=auth_schemas.TokenResponse)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
  user = user_repository.get_by_email(db, email=form_data.email)

  if not user or not security.verify_password(form_data.password, user.hashed_password):
       raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
       )
  
  access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  token = security.create_access_token(
            subject=user.id, expires_delta=access_token_expires
        )
  return {
      "access_token": token,
      "token_type": "bearer",
      "user": user
  }
