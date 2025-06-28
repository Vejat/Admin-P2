from sqlalchemy import Column, Integer, String, Enum
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, nullable=False)
    status = Column(Enum("pendiente", "en_progreso", "completada", name="task_status"), default="pendiente")
