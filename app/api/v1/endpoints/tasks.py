from math import ceil
from fastapi import APIRouter,Query,Body, HTTPException,Path,status, Depends
from app.schemas import task as task_schemas
from typing import Optional, Literal, Any
from sqlalchemy.orm import Session
from app.repositories.task_repository import task_repository
from app.models.user import User
from app.api.v1 import deps
router = APIRouter()

@router.get("/", response_model=task_schemas.PaginatedTaskResponse)
def get_tasks(query: Optional[str] = Query(
    default = None,
    description="Search query for task title",
    alias="query",
    min_length=3,
    max_length=50,
    pattern="^[a-zA-Z]+$",
    ),
    per_page : int = Query(
        6,
        ge=1,
        le=50,
        description="Maximum number of tasks to return by page"
    ),
    page: int = Query(
        1, ge=1,
        description="Número de página (>=1)"
    ),
    order_by: Literal["id"]  = Query(
        "id",
        description="Field to order tasks by"
    ),
    direction: Literal["asc","desc"] = Query(
        "asc",
        description="Order direction"),
    ):
    filtered_data = []
    if query:
        filtered_data = [t for t in [] if query.lower() in t["id"].lower()]
    
    is_reverse = (direction == "desc")
    sorted_data = sorted(
        filtered_data, 
        key=lambda x: x[order_by], 
        reverse=is_reverse
    )
    
    total = len(sorted_data)
    total_pages = ceil(total / per_page) if total > 0 else 0
    current_page = min(page, total_pages) if total_pages > 0 else 1
    
    start = (current_page - 1) * per_page
    items = sorted_data[start : start + per_page] 

    return {
        "page": current_page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "has_prev": current_page > 1,
        "has_next": current_page < total_pages,
        "order_by": "id",
        "direction": "desc",
        "query": query,
        "tasks": items  
    }

@router.post("/", response_model=task_schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    task_in: task_schemas.TaskCreate,
    current_user: User = Depends(deps.get_current_active_user) 
) -> Any:
    new_task = task_repository.create_with_owner(
        db, 
        obj_in=task_in, 
        user_id=current_user.id
    )
    
    return new_task
# @router.put("/{task_id}", response_model = task_schemas.TaskResponse, response_description="The updated task")
# def update_task(task_id: int=Path(
#     ...,
#     ge=1,
#     title="Task ID",
#     description="The ID of the task to update",
#     example=1
# ), data: task_schemas.TaskUpdate=Body(...)):
#     for task in TASKS:
#         if task["id"] == task_id:
#             if "title" in data:task["title"] = data["title"]
#             if "description" in data:task["description"] = data["description"]
#             if "priority" in data:task["priority"] = data["priority"]
#             if "is_completed" in data:task["is_completed"] = data["is_completed"]
#             return task
#     return HTTPException(status_code=404, detail="Task not found")    


# @router.delete("/{task_id}")
# def delete_task(task_id: int):
#     for task in TASKS:
#         if task["id"] == task_id:
#             TASKS.remove(task)
#             return {"msg": f"Task {task_id} deleted successfully"}
#     raise HTTPException(status_code=404, detail="Task not found")


