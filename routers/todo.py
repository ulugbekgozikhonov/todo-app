from fastapi import APIRouter, HTTPException

from general import db_dependency, token_dependency
from models import Task
from routers.auth import get_current_user
from schemas import TaskRequest

router = APIRouter(tags=["todo"], prefix="/todo")


@router.get(path="/list")
async def todo_list(db: db_dependency, token: token_dependency):
	user = get_current_user(token)
	print(user)
	if user is None:
		raise HTTPException(status_code=401, detail="Unauthorized")

	tasks = db.query(Task).filter(Task.owner_id == user.id).all()
	return tasks


@router.get(path="/{id}",status_code=200)
async def todo_by_id(id: int, db: db_dependency, token: token_dependency):
	task = db.query(Task).filter(Task.id == id).first()
	if task is None:
		raise HTTPException(status_code=404, detail="Task not found")
	return task


@router.post(path="/create", status_code=201)
async def create_task(task_request: TaskRequest, db: db_dependency):
	try:
		task = Task(**task_request.model_dump())
		db.add(task)
		db.commit()
		return task_request
	except Exception as e:
		raise HTTPException(status_code=400, detail=f"{e}")


@router.put(path="/update/{id}", status_code=200)
async def update_task(task_id: int, task_request: TaskRequest, db: db_dependency):
	task = db.query(Task).filter(Task.id == task_id).first()
	if not task:
		raise HTTPException(status_code=404, detail="Not Found")

	for key, val in task_request.model_dump().items():
		setattr(task, key, val)

	db.commit()

	return "Successfully updated"
