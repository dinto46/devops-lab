from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import Base, SessionLocal, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Devops Task Manager")


class TaskCreate(BaseModel):
	title: str
	description: str = ""
	completed: bool = False


class TaskResponse(TaskCreate):
	id: int

	class config:
		from_attributes = True

def get_db():
	db = SessionLocal()

	try:
		yield db
	finally:
		db.close()

@app.get("/")
def root():
	return{
		"message": "DevOps Task Manager API"
	}

@app.get("/health")
def health_check():
	return{
		"status": "healthy"
	}
@app.get("/tasks", response_model = list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
	return db.query(models.Task).all()

@app.get("/tasks/{task_id}", response_model = list[TaskResponse])
def get_task(task_id: int, db: Session = Depends(get_db)):
	task = db.query(models.Task).filter(
		models.Task.id == task_id
	).first()

	if not task:
		raise HTTPException(
			status_code = 404,
			detail = "Task not found"
		)
	return task


@app.post("/tasks", response_model = TaskResponse)
def create_task(
	task: TaskCreate,
	db: Session = Depends(get_db)
):
	new_task = models.Task(
		title = task.title,
		description = task.description,
		completed = task.completed
	)

	db.add(new_task)
	db.commit()
	db.refresh(new_task)

	return new_task


@app.put("/tasks/{task_id}", response_model = TaskResponse)
def update_task(
	task_id: int,
	updated_task: TaskCreate,
	db: Session = Depends(get_db)
):
	task = db.query(models.Task).filter(
		models.Task.id == task_id
	).first()

	if not task:
		raise HTTPException(
			status_code=404,
			detail="Task not found"
		)

	title = task.title
	description = task.description
	completed = task.completed

	db.commit()
	db.refresh(task)

	return task


@app.delete("/tasks/{task_id}")
def delete_task(
	task_id: int,
	db: Session = Depends(get_db)
):
	tasks = db.query(models.Task).filter(
		models.Task.id == task_id
	).first()

	if not Task:
		raise HTTPException(
			status_code=404, 
			detail="Task not found"
		)

	db.delete(Task)
	db.commit()

	return{
		"message": "Task deleted"
	}
