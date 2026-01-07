from pydantic import BaseModel,Field
from typing import List

class CategorieBase(BaseModel):
    name: str = Field(...,min_length=1, max_length=100, description="Name of the categorie")
    
class CategorieCreate(CategorieBase):
    pass
class CategorieResponse(CategorieBase):
    id: int
class CategorieListResponse(BaseModel):
    categories: List[CategorieResponse]

