from fastapi import FastAPI

from database import engine
from models import Base
from routers import auth,todo

Base.metadata.create_all(bind=engine)
app = FastAPI(title="TODOS API")

@app.get("/ketmon",status_code=200)
async def ketmon():
	return {"success": True}

app.include_router(auth.router)
app.include_router(todo.router)
