import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import SessionLocal, engine, Base 
from app.models.category import Category
from app.api.v1.api_router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea tabas
    Base.metadata.create_all(bind=engine)
    
    # Seed 
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

app = FastAPI(
    title="Todo App API",
    version="1.0.0",
    lifespan=lifespan
)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok"}