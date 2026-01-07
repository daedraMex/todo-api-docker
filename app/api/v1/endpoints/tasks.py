from fastapi import APIRouter,Query,Body, HTTPException,Path
from app.schemas import task as task_schemas
from typing import List,Optional, Literal
router = APIRouter()

TASKS = [
    {"id": 1, "title": "Task 1", "description": "Description for Task 1", "is_completed": False},
    {"id": 2, "title": "Task 2", "description": "Description for Task 2", "is_completed": True},
    {"id": 3, "title": "Task 3", "description": "Description for Task 3", "is_completed": False},
    {"id": 4, "title": "Task 4", "description": "Description for Task 4", "is_completed": True},
    {"id": 5, "title": "Task 5", "description": "Description for Task 5", "is_completed": False},
    {"id": 6, "title": "Task 6", "description": "Description for Task 6", "is_completed": True},
    {"id": 7, "title": "Task 7", "description": "Description for Task 7", "is_completed": False},
    {"id": 8, "title": "Task 8", "description": "Description for Task 8", "is_completed": True},
    {"id": 9, "title": "Task 9", "description": "Description for Task 9", "is_completed": False},
    {"id": 10, "title": "Task 10", "description": "Description for Task 10", "is_completed": True},
]

@router.get("/", response_model=List[task_schemas.PagintedTaskResponse])
def get_tasks(query: Optional[str] = Query(
    default = None,
    description="Search query for task title",
    alias="query",
    min_length=3,
    max_length=50,
    regex="^[a-zA-Z]+$",
    ),
    limit : int = Query(
        6,
        ge=1,
        le=50,
        description="Maximum number of tasks to return by page"
    ),
    offset : int = Query(
        0,
        ge=0,
        le=1000,
        description="Number of tasks to skip for pagination" 
    ), 
    order_by: Literal["id"]  = Query(
        "id",
        description="Field to order tasks by"
    ),
    direction: Literal["asc","desc"] = Query(
        "asc",
        description="Order direction"),
    ):
    filtered_data = TASKS
    if query:
        filtered_data = [t for t in TASKS if query.lower() in t["title"].lower()]
    
    is_reverse = (direction == "desc")

    sorted_data = sorted(
        filtered_data, 
        key=lambda x: x[order_by], 
        reverse=is_reverse
    )
    
    results = sorted_data[offset : offset + limit]
    total = len(filtered_data)
    
    return task_schemas.PagintedTaskResponse(
        page=(offset // limit) + 1,
        per_page=limit,

        total=total,
        total_pages=(total + limit - 1) // limit,
        has_prev=offset > 0,
        has_next=offset + limit < total,
        order_by=order_by,
        direction=direction,
        query=query,
        tasks=results
    )


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


