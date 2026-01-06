from fastapi import APIRouter,Query

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

@router.post("/tasks")
def create_task():
    return {"msg": "Task created successfully"}

def delete_task(task_id: int):
    return {"msg": f"Task {task_id} deleted successfully"}

