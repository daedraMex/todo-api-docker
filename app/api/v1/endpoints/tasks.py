from fastapi import APIRouter

router = APIRouter()

TASKS = [
    {"id": 1, "title": "Task 1", "completed": False},
    {"id": 2, "title": "Task 2", "completed": True},
]
@router.get("/tasks")
def get_tasks():
    return {"data": TASKS}

@router.post("/tasks")
def create_task():
    return {"msg": "Task created successfully"}

def delete_task(task_id: int):
    return {"msg": f"Task {task_id} deleted successfully"}

