from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx

from . import models, schemas, crud
from .database import SessionLocal, engine, Base
import os
from dotenv import load_dotenv

load_dotenv()
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000/users/")

Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/api/tasks")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "task-service running"}
@app.get("/env")
def show_env():
    return {
        "DB_NAME": os.getenv("DB_NAME"),
        "USER_SERVICE_URL": os.getenv("USER_SERVICE_URL")
    }
@app.post("/tasks", response_model=schemas.TaskRead)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}{task.user_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return crud.create_task(db, task)

@app.get("/tasks", response_model=list[schemas.TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@app.get("/tasks/{task_id}", response_model=schemas.TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

@app.put("/tasks/{task_id}", response_model=schemas.TaskRead)
def update_status(task_id: int, update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = crud.update_task_status(db, task_id, update.status)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

@app.get("/tasks/", response_model=list[schemas.TaskRead])
def get_tasks_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_tasks_by_user(db, user_id)
