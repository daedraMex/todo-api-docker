from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import engine, Base
from app.api.v1.api_router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Ciclo de vida de la aplicación:
    Se ejecuta al iniciar el servidor para preparar la infraestructura.
    """
    # 1. Creación de tablas en PostgreSQL (Categorie, Task, User)
    Base.metadata.create_all(bind=engine)
    
    yield # Aquí es donde la aplicación corre
    
    # Lógica de apagado (si fuera necesaria) se colocaría aquí

# Inicialización de FastAPI con lifespan
app = FastAPI(
    title="TaskFlow API",
    description="Backend para gestión de tareas con Atomic Design y Clean Architecture",
    version="1.0.0",
    lifespan=lifespan
)

# --- Configuración de CORS ---
# Permite la comunicación segura con tu frontend de Vite
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

# --- Registro de Rutas ---

# 1. Rutas principales de la API (Tasks, Auth, Users)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "TaskFlow API is running",
        "docs": "/docs",
        "version": "1.0.0"
    }