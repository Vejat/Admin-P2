from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    user_id: int

class TaskUpdate(BaseModel):
    status: str

class TaskRead(TaskCreate):
    id: int
    status: str

    class Config:
        orm_mode = True
