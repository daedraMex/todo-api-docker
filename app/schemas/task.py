from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=500, description="Descripción detallada")
    status: Optional[str] = Field("pending", description="Estado inicial de la tarea")
    category_id: int = Field(..., description="ID de la categoría asociada")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    color: Optional[str] = Field(None, description="Color hexadecimal asignado")
    priority: Optional[str] = Field("medium", description="Prioridad: low, medium, high")
    status: Optional[str] = Field("pending")
    is_completed: Optional[bool] = Field(False)

class TaskResponse(TaskBase):
    id: int
    title: str
    status: str
    color: str
    user_id: int
    categorie_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
class PaginatedTaskResponse(BaseModel): # Asegúrate que tenga la 'a'
    page: int
    per_page: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    order_by: Literal["id"]
    direction: Literal["asc", "desc"]
    query: Optional[str] = None
    tasks: List[TaskResponse]