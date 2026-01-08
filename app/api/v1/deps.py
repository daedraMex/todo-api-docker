from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db as _get_db # Lo traemos de core
from app.models.user import User

def get_db() -> Generator:
    yield from _get_db()

def get_current_active_user(
    db: Session = Depends(get_db),
    # token: str = Depends(...) logic aquí
) -> User:
    # Tu lógica de seguridad aquí
    pass