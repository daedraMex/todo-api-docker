import os
from contextlib import asynccontextmanager
from fastapi import FastAPI

# 1. Fix del typo (sin espacio)
from app.database import SessionLocal, engine, Base 
from app.models.category import Category
from app.api.v1.api_router import api_router

# 2. Definir lifespan PRIMERO
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    # Seeding
    db = SessionLocal()
    try:
        init_categories = ["Trabajo", "Estudio", "Casa", "Familia", "Diversión"]
        for name in init_categories:
            if not db.query(Category).filter(Category.name == name).first():
                db.add(Category(name=name))
        db.commit()
    finally:
        db.close()
    yield

# 3. Crear la app pasando el lifespan
app = FastAPI(
    title="Todo App API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok"}