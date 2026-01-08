from fastapi import APIRouter
from .endpoints import auth, tasks, categories, utils

api_router = APIRouter()

api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(utils.router, prefix="/utils", tags=["Utils"])