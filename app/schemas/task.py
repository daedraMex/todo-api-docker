from pydantic import BaseModel,Field
from typing import Optional,List

class TaskBase(BaseModel):
    title: str = Field(...,min_length=1, max_length=100, description="Title of the task")
    description: Optional[str] = "[ Write something short about the task ]"
    is_completed: Optional[bool] = False
    priority: Optional[str] = "medium"
    status: Optional[str] = "pending"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title:str =Field(...,min_length=1, max_length=100, description="Title of the task")
    description: Optional[str] = Field(None, max_length=500, description="Description of the task")
    priority: Optional[str] = Field("medium", description="Priority of the task: low, medium, high")
    status: Optional[str] = Field("pending", description="Status of the task")
    is_completed: Optional[bool] = False

class TaskResponse(TaskBase):
    id: int

class PagintedTaskResponse(BaseModel):
    page:int
    per_page:int
    total: int
    total_pages:int
    has_prev: bool
    has_next: bool
    order_by: str
    direction: str
    query: Optional[str]
    tasks: List[TaskResponse]