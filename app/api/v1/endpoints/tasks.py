from fastapi import APIRouter,Query,Body, HTTPException
from app.schemas import task as task_schemas

router = APIRouter()

TASKS = [
    {"id": 1, "title": "Task 1", "completed": False},
    {"id": 2, "title": "Task 2", "completed": True},
]
@router.get("/")
def get_tasks(query: str | None= Query(default = None,description="Search query for task title")):
    if query:
      filtered_tasks = []
      for task in TASKS:
         if query.lower() in task["title"].lower():
            filtered_tasks.append(task)
        
      return {"data": filtered_tasks, "query": query}
    
    return {"data": TASKS}


@router.post("/")
def create_task( task: task_schemas.TaskCreate):
  
  
    return {"msg": "Task created successfully"}

@router.put("/{task_id}")
def update_task(task_id: int,data: task_schemas.TaskUpdate ):
    for task in TASKS:
        if task["id"] == task_id:
            if "title" in data:task["title"] = data["title"]
            if "description" in data:task["description"] = data["description"]
            if "priority" in data:task["priority"] = data["priority"]
            if "completed" in data:task["completed"] = data["completed"]
            return {"msg": f"Task {task_id} updated successfully"}
    raise HTTPException(status_code=404, detail="Task not found")    


@router.delete("/{task_id}")
def delete_task(task_id: int):
    for task in TASKS:
        if task["id"] == task_id:
            TASKS.remove(task)
            return {"msg": f"Task {task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")


