from fastapi import FastAPI

from database import engine
from models import Base
import auth
import todo

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TODOS API")

app.include_router(auth.router)
app.include_router(todo.router)
