import random
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.task import Task
from app.schemas.task import TaskCreate

class TaskRepository(BaseRepository[Task, TaskCreate]):
    
    def _generate_random_hex_color(self) -> str:
        """color headecimal random."""
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def _get_unique_color_for_user(self, db: Session, user_id: int) -> str:
        """crea un color unico para los tas"""
        while True:
            color = self._generate_random_hex_color()
            # si ya existe
            stmt = select(Task).where(Task.user_id == user_id, Task.color == color)
            exists = db.execute(stmt).scalars().first()
            if not exists:
                return color

    def create_with_owner(self, db: Session, *, obj_in: TaskCreate, user_id: int) -> Task:
        """ color único y asigna el dueño """
        unique_color = self._get_unique_color_for_user(db, user_id)
        
        db_obj = Task(
            **obj_in.model_dump(),
            user_id=user_id,
            color=unique_color
        )
        
        return self.save(db, db_obj)

task_repository = TaskRepository(Task)