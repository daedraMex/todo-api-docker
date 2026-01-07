import os
from datetime import datetime, timedelta, timezone
from typing import Literal, Optional
from click import pass_context
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, PyJWTError
from pwdlib import PasswordHash
from sqlmodel import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User


# from app.api.v1.auth.repository import UserRepository


password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

credentials_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Cannot validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)


def raise_expired_token():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expired",
        headers={"WWW-Authenticate": "Bearer"}
    )


def raise_forbidden():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient permissions",
    )


def invalid_credentials():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Invalid credentials")


def decode_token(token: str) -> dict:
    playload = jwt.decode(
        jwt=token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    return playload


def create_access_token(sub: str, minutes: int | None = None) -> str:
    expire = datetime.now(
        timezone.utc) + timedelta(minutes=minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": sub, "exp": expire}, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:

    try:
        playload = decode_token(token)
        sub: Optional[str] = playload.get("sub")
        if not sub:
            raise credentials_exc

        user_id = int(sub)
    except ExpiredSignatureError:
        raise raise_expired_token()
    except InvalidTokenError:
        raise credentials_exc
    except PyJWTError:
        raise invalid_credentials()

    user = db.get(User, user_id)

    if not user or not user.is_active:
        raise invalid_credentials()

    return user


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


def require_role(min_role: Literal["user", "admin"]):
    order = {"user": 0, "admin": 1}

    def evaluation(user: User = Depends(get_current_user)) -> User:
        if order[user.role] < order[min_role]:
            raise raise_forbidden()
        return user

    return evaluation


async def auth2_token(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    repository = UserRepository(db)
    user = repository.get_by_email(form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise invalid_credentials()
    token = create_access_token(sub=str(user.id))
    return {"access_token": token, "token_type": "bearer"}

require_user = require_role("user")
require_admin = require_role("admin")