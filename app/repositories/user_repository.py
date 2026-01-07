from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.models.user import User
from app.schemas.auth import UserCreate


class UserRepository(BaseRepository[User, UserCreate]):
    
    def create_user(self, db: Session, *, obj_in: UserCreate, hashed_password: str) -> User:
        db_obj_data = obj_in.model_dump(exclude={"password"})
        
        db_obj = self.model(**db_obj_data, hashed_password=hashed_password)
        
        if not db_obj.role:
            db_obj.role = "user"
            
        return self.save(db, db_obj)
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        statement = select(self.model).where(self.model.email == email)
        result = db.execute(statement).scalars().first()
        return result
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        statement = select(self.model).where(self.model.username == username)
        result = db.execute(statement).scalars().first()
        return result
    
user_repository = UserRepository(User)