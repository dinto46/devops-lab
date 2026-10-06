from fastapi import FastAPI,HTTPException
from pydantic import BaseModel


app = FastAPI(title="Devops Task Manager")


class Task(BaseModel):
	title: str
	description: str = ""
	completed: bool = False

tasks =[]
next_id = 1

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
@app.get("/tasks")
def get_tasks():
	return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
	for task in tasks:
		if task["id"] == task_id:
			return task

	raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def create_task(task: Task):
	global next_id

	new_task = {
		"id": next_id,
		**task.model_dump()
	}

	tasks.append(new_task)
	next_id += 1

	return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
	for task in tasks:
		if task["id"] == task_id:
			task.update(updated_task.model_dump())
			return task

	raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
	for task in tasks:
		if task["id"] == task_id:
			tasks.remove(task)
			return{
				"message": "Task Deleted"
			}

	raise HTTPException(status_code=404, detail="Task not found")
