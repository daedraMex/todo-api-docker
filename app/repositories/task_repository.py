import random
from sqlalchemy import select,func
from sqlalchemy.orm import Session, joinedload
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

        saved_task = self.save(db, db_obj)

        # Recargar con la relación category
        stmt = select(Task).options(joinedload(Task.category)).where(Task.id == saved_task.id)
        return db.execute(stmt).unique().scalars().first()
    def get_multi_by_owner(
        self, db: Session, *, user_id: int, page: int = 1, per_page: int = 6, query: str = None, order_by: str = "id", direction: str = "asc"
    ):
        """Obtiene tareas pagiadas filtrando por el dueño (user_id)."""
        stmt = select(Task).options(joinedload(Task.category)).where(Task.user_id == user_id)

        if query:
            stmt = stmt.where(Task.title.ilike(f"%{query}%"))

        total = db.execute(select(func.count()).select_from(stmt.subquery())).scalar()

        skip = (page - 1) * per_page

        order_field = getattr(Task, order_by, Task.id)

        if direction == "desc":
            stmt = stmt.order_by(order_field.desc())
        else:
            stmt = stmt.order_by(order_field.asc())

        stmt = stmt.offset(skip).limit(per_page)

        items = db.execute(stmt).unique().scalars().all()
        return items, total

    def get_by_owner(self, db: Session, *, task_id: int, user_id: int) -> Task | None:
        """Obtiene una tarea por ID verificando que pertenezca al usuario."""
        stmt = select(Task).options(joinedload(Task.category)).where(Task.id == task_id, Task.user_id == user_id)
        return db.execute(stmt).unique().scalars().first()

    def update(self, db: Session, *, db_obj: Task, obj_in: dict) -> Task:
        """Actualiza una tarea con los datos proporcionados."""
        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)
        updated_task = self.save(db, db_obj)

        stmt = select(Task).options(joinedload(Task.category)).where(Task.id == updated_task.id)
        return db.execute(stmt).unique().scalars().first()

task_repository = TaskRepository(Task)