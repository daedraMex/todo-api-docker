from fastapi import APIRouter,Query,Body, HTTPException,Path
from app.schemas import task as task_schemas
from typing import List,Optional
router = APIRouter()

TASKS = [
    {"id": 1, "title": "Task 1", "description": "Description for Task 1", "is_completed": False},
    {"id": 2, "title": "Task 2", "description": "Description for Task 2", "is_completed": True},
]

@router.get("/", response_model=List[task_schemas.TaskResponse])
def get_tasks(query: Optional[str] = Query(
    default = None,
    description="Search query for task title",
    alias="query",
    min_length=3,
    max_length=50,
    regex="^[a-zA-Z]+$",
    )):
    if query:
      filtered_tasks = []
      for task in TASKS:
         if query.lower() in task["title"].lower():
            filtered_tasks.append(task)
        
      return  filtered_tasks
    
    return TASKS


@router.post("/")
def create_task( task: task_schemas.TaskCreate):
  
  
    return {"msg": "Task created successfully"}

@router.put("/{task_id}", response_model = task_schemas.TaskResponse, response_description="The updated task")
def update_task(task_id: int=Path(
    ...,
    ge=1,
    title="Task ID",
    description="The ID of the task to update",
    example=1
), data: task_schemas.TaskUpdate=Body(...)):
    for task in TASKS:
        if task["id"] == task_id:
            if "title" in data:task["title"] = data["title"]
            if "description" in data:task["description"] = data["description"]
            if "priority" in data:task["priority"] = data["priority"]
            if "is_completed" in data:task["is_completed"] = data["is_completed"]
            return task
    return HTTPException(status_code=404, detail="Task not found")    


@router.delete("/{task_id}")
def delete_task(task_id: int):
    for task in TASKS:
        if task["id"] == task_id:
            TASKS.remove(task)
            return {"msg": f"Task {task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")


