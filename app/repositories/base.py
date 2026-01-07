from typing import Generic, Type, TypeVar, List, Optional
from sqlmodel import Session, select

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")

class BaseRepository(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.get(self.model, id)

    def get_multi(self, db: Session, * , skip: int = 0, limit: int = 100) -> List[ModelType]:
        statement = select(self.model).offset(skip).limit(limit)
        return db.exec(statement).all()
    
    def save(self, db: Session, db_obj: ModelType) -> ModelType:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model.model_validate(obj_in)
        return self.save(db, db_obj)