from pydantic import BaseModel,Field
from typing import Optional

class TaskBase(BaseModel):
    id: int
    title: str = Field(...,min_length=1, max_length=100, description="Title of the task")
    description: Optional[str] = None
    completed: bool = False
    priority: str
    status: str

class TaskCreate(BaseModel):
    title: str = Field(...,min_length=1, max_length=100, description="Title of the task")
    description: Optional[str] = Field(None, max_length=500, description="Description of the task")
    priority: str = Field(..., description="Priority of the task: low, medium, high")
    status: Optional[str] = Field("pending", description="Status of the task")


class TaskResponse(TaskBase):
    id: int
    color: str
    is_finished: bool

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None,min_length=1, max_length=100, description="Title of the task")
    description: Optional[str] = Field(None, max_length=500, description="Description of the task")
    priority: Optional[str] = Field(None, description="Priority of the task: low, medium, high")
    status: Optional[str] = Field(None, description="Status of the task")
    completed: Optional[bool] = None
    