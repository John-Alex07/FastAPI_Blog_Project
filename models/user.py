from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    tags: List[str] = []

    class Config:
        orm_mode = True
        
class BlogPost(BaseModel):
    title: str
    content: str
    author: str
    tags: List[str] = []
    created_at: datetime = datetime.now()

    class Config:
        orm_mode = True

class UserInDB(User):
    id: str
    hashed_password: str

# Model for creating a new user
class UserCreate(User):
    password: str

# Model for updating user profile
class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    tags: Optional[List[str]] = []