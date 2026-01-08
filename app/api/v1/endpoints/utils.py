from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.v1 import deps
from app.db.seed import seed_db as run_seed

router = APIRouter()

@router.post("/seed", status_code=status.HTTP_201_CREATED)
def seed_database(db: Session = Depends(deps.get_db)):

    return run_seed(db)