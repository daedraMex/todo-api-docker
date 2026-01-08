from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Literal

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username of the user")
    email: EmailStr = Field(..., description="Email address of the user")
   

Role = Literal["admin", "user"]

class UserPublic(UserBase):
    id: int
    role: Role

class UserCreate(BaseModel):
    password: str = Field(..., min_length=6,  max_length=50,description="Password for the user")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(..., min_length=6, max_length=50, description="Password for the user")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
class UserResponse(UserBase):
    id: int
    role: str
    
    class Config:
        from_attributes = True

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse