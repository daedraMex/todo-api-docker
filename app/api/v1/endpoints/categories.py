from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db # Asegúrate de que NO haya espacios aquí
from app.models.category import Category
from app.schemas import categorie as categorie_schemas

router = APIRouter()

@router.get("/", response_model=categorie_schemas.CategorieListResponse)
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return {"categories": categories}

@router.post("/", response_model=categorie_schemas.CategorieResponse)
def create_category(
    category: categorie_schemas.CategorieCreate,
    db: Session = Depends(get_db)
):
    db_category = db.query(Category).filter(Category.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {"category": new_category}
