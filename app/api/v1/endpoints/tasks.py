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
def get_tasks(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    query: Optional[str] = Query(None, min_length=3, max_length=50),
    page: int = Query(1, ge=1),
    per_page: int = Query(6, ge=1, le=50),
    order_by: Literal["id", "created_at"] = Query("id", description="Field to order tasks by"),
    direction: Literal["asc", "desc"] = Query("asc", description="Order direction")
):

    items, total = task_repository.get_multi_by_owner(
        db,
        user_id=current_user.id,
        page=page,
        per_page=per_page,
        query=query,
        order_by=order_by,
        direction=direction
    )

    total_pages = ceil(total / per_page) if total > 0 else 0

    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "has_prev": page > 1,
        "has_next": page < total_pages,
        "order_by": order_by,
        "direction": direction,
        "query": query,
        "tasks": items
    }
# def get_tasks(query: Optional[str] = Query(
#     default = None,
#     description="Search query for task title",
#     alias="query",
#     min_length=3,
#     max_length=50,
#     pattern="^[a-zA-Z]+$",
#     ),
#     per_page : int = Query(
#         6,
#         ge=1,
#         le=50,
#         description="Maximum number of tasks to return by page"
#     ),
#     page: int = Query(
#         1, ge=1,
#         description="Número de página (>=1)"
#     ),
#     order_by: Literal["id"]  = Query(
#         "id",
#         description="Field to order tasks by"
#     ),
#     direction: Literal["asc","desc"] = Query(
#         "asc",
#         description="Order direction"),
#     ):
#     filtered_data = []
#     if query:
#         filtered_data = [t for t in [] if query.lower() in t["id"].lower()]
    
#     is_reverse = (direction == "desc")
#     sorted_data = sorted(
#         filtered_data, 
#         key=lambda x: x[order_by], 
#         reverse=is_reverse
#     )
    
#     total = len(sorted_data)
#     total_pages = ceil(total / per_page) if total > 0 else 0
#     current_page = min(page, total_pages) if total_pages > 0 else 1
    
#     start = (current_page - 1) * per_page
#     items = sorted_data[start : start + per_page] 

#     return {
#         "page": current_page,
#         "per_page": per_page,
#         "total": total,
#         "total_pages": total_pages,
#         "has_prev": current_page > 1,
#         "has_next": current_page < total_pages,
#         "order_by": "id",
#         "direction": "desc",
#         "query": query,
#         "tasks": items  
#     }

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

@router.put("/{task_id}", response_model=task_schemas.TaskResponse)
def update_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int = Path(..., ge=1, description="The ID of the task to update"),
    task_in: task_schemas.TaskUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Actualiza una tarea existente."""
    task = task_repository.get_by_owner(db, task_id=task_id, user_id=current_user.id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )

    update_data = task_in.model_dump(exclude_unset=True)
    updated_task = task_repository.update(db, db_obj=task, obj_in=update_data)

    return updated_task

@router.patch("/{task_id}/complete", response_model=task_schemas.TaskResponse)
def toggle_task_completion(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int = Path(..., ge=1, description="The ID of the task to toggle completion"),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Marca o desmarca una tarea como completada."""
    task = task_repository.get_by_owner(db, task_id=task_id, user_id=current_user.id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )

    update_data = {"is_completed": not task.is_completed}
    updated_task = task_repository.update(db, db_obj=task, obj_in=update_data)

    return updated_task

# @router.delete("/{task_id}")
# def delete_task(task_id: int):
#     for task in TASKS:
#         if task["id"] == task_id:
#             TASKS.remove(task)
#             return {"msg": f"Task {task_id} deleted successfully"}
#     raise HTTPException(status_code=404, detail="Task not found")


