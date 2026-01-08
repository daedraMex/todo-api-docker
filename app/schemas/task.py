from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime

class CategoryInTask(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=500, description="Descripción detallada")
    category_id: int = Field(..., description="ID de la categoría asociada")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    color: Optional[str] = Field(None, description="Color hexadecimal asignado")
    priority: Optional[str] = Field("medium", description="Prioridad: low, medium, high")
    is_completed: Optional[bool] = Field(False)

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    color: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: int
    category_id: int
    category: CategoryInTask

    class Config:
        from_attributes = True
class PaginatedTaskResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    order_by: Literal["id", "created_at"]
    direction: Literal["asc", "desc"]
    query: Optional[str] = None
    tasks: List[TaskResponse]