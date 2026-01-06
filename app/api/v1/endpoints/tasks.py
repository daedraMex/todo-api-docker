from fastapi import APIRouter,Query,Body, HTTPException

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
def create_task(task:dict = Body(...)):
    if "title" not in task or "description" not in task or "priority" not in task:
        return {"error": "Title, description, and priority are required fields."}

    if not str(task["title"]).strip():
        return {"error": "Title cannot be empty."}
    
    if "description" in task and len(task["description"]) > 500:
        return {"error": "Description cannot exceed 500 characters."}
    if task["priority"] not in ["low", "medium", "high"]:
        return {"error": "Priority must be one of: low, medium, high."}
    
    new_id = TASKS[-1]["id"] + 1 if TASKS else 1

    new_task = {
        "id": new_id,
        "title": task["title"],
        "description": task["description"],
        "priority": task["priority"],
        "completed": False
    }
    TASKS.append(new_task)
    return {"msg": "Task created successfully"}

@router.put("/{task_id}")

def update_task(task_id: int,data:dict = Body(...)):
    for task in TASKS:
        if task["id"] == task_id:
            if "title" in data:task["title"] = data["title"]
            if "description" in data:task["description"] = data["description"]
            if "priority" in data:task["priority"] = data["priority"]
            if "completed" in data:task["completed"] = data["completed"]
            return {"msg": f"Task {task_id} updated successfully"}
    raise HTTPException(status_code=404, detail="Task not found")    



def delete_task(task_id: int):
    return {"msg": f"Task {task_id} deleted successfully"}


