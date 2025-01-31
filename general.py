from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
dependency = Annotated[Session, Depends(get_db)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")