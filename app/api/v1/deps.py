from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db as _get_db # Lo traemos de core
from app.core.security import get_current_user
from app.models.user import User

def get_db() -> Generator:
    yield from _get_db()

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    return current_user