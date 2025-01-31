from fastapi import APIRouter,HTTPException,Depends
from models import Task
from schemas import TaskRequest
from general import dependency,oauth2_scheme
from auth import decode_access_token
from typing import Annotated


router = APIRouter(tags=["todo"],prefix="/todo")

@router.get(path="/list")
async def todo_list(db: dependency,token: Annotated[str,Depends(oauth2_scheme)]):
    payload = decode_access_token(token)
    tasks = db.query(Task).all()
    return tasks
    
    
        
@router.post(path="/create",status_code=201)
async def create_task(task_request: TaskRequest,db: dependency):
    try:
        task = Task(**task_request.model_dump())
        db.add(task)
        db.commit()
        return task_request
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"{e}")


@router.put(path="/update/{id}",status_code=200)
async def update_task(task_id: int,task_request: TaskRequest,db:dependency):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404,detail="Not Found")
    
    for key,val in task_request.model_dump().items():
        setattr(task,key,val)

    db.commit()
    
    return "Successfully updated"