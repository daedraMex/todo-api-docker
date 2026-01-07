from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db # Asegúrate de que NO haya espacios aquí
from app.models.category import Category
from app.schemas import categorie as categorie_schemas

router = APIRouter()

@router.get("/", response_model=categorie_schemas.CategorieListResponse)
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return {"categories": categories}