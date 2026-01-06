from fastapi import FastAPI
from app.api.v1.api_router import api_router

import os

app = FastAPI(title="Todo App API", version="1.0.0")

#Concateno api/v1 a las rutas
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok", "version": "1.0.0"}