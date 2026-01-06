from fastapi import APIRouter
from datetime import timedelta


router = APIRouter()

@router.post("/register")
def register(user_data):
    # Lógica para registrar un nuevo usuario
    return {"msg": "User registered successfully"}
@router.post("/login")
def login():
    # Lógica para autenticar al usuario y generar un token JWT
    return {"access_token": "fake-jwt-token", "token_type": "bearer"}

