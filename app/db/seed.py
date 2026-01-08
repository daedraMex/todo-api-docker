import random
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.category import Category as Categorie
from app.models.task import Task
from app.core.security import get_password_hash

def generate_unique_color(db: Session, user_id: int) -> str:
    """Genera un color hexadecimal único para las tareas del usuario."""
    while True:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        stmt = select(Task).where(Task.user_id == user_id, Task.color == color)
        if not db.execute(stmt).scalars().first():
            return color

def seed_db(db: Session = None): 
    local_session = False
    if db is None:
        db = SessionLocal()
        local_session = True
    
    try:
        user_email = "user@gmail.com"
        user = db.execute(select(User).where(User.email == user_email)).scalar_one_or_none()
        
        if not user:
            user = User(
                email=user_email,
                username="Jane Doe",
                hashed_password=get_password_hash("secret123"),
                role="user"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print("✅ Usuario listo.")

        cats_names = ["Trabajo", "Estudio", "Casa", "Familia", "Diversión"]
        
        for name in cats_names:
            stmt = select(Categorie).where(Categorie.name == name, Categorie.user_id == user.id)
            if not db.execute(stmt).scalars().first():
                db.add(Categorie(name=name, user_id=user.id))
        
        db.commit()
        
        all_categories = db.execute(select(Categorie).where(Categorie.user_id == user.id)).scalars().all()

        tasks_to_seed = [
            {"title": "Finalizar reporte trimestral", "description": "Revisar KPIs y métricas de Q4"},
            {"title": "Preparar examen de React", "description": "Repasar Hooks y Context API"},
            {"title": "Organizar el garaje", "description": "Separar cajas para reciclaje"},
            {"title": "Cena de cumpleaños", "description": "Reservar mesa para 6 personas"},
            {"title": "Sesión de gaming", "description": "Terminar la campaña de fin de semana"},
            {"title": "Comprar víveres", "description": "Enfoque en frutas y verduras frescas"},
            {"title": "Llamada con el equipo", "description": "Sincronización de tareas semanales"}
        ]

        for t_data in tasks_to_seed:
            task_exists = db.execute(
                select(Task).where(Task.title == t_data["title"], Task.user_id == user.id)
            ).scalar_one_or_none()

            if not task_exists:
                random_cat = random.choice(all_categories)

                new_task = Task(
                    **t_data,
                    color=generate_unique_color(db, user.id),
                    user_id=user.id,
                    category_id=random_cat.id,
                    is_completed=False
                )
                db.add(new_task)
                print(f"✅ Tarea '{t_data['title']}' asignada a '{random_cat.name}'")
        
        db.commit()
        print("🚀 Seed finalizado con éxito.")
        return {"status": "success", "message": "Database seeded"}
    
    except Exception as e:
        print(f"❌ Error durante el seed: {e}")
        db.rollback()
        raise e
    finally:
        if local_session:
            db.close()

if __name__ == "__main__":
    seed_db()