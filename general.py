from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import SessionLocal


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


db_dependency = Annotated[Session, Depends(get_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")
token_dependency = Annotated[str, Depends(oauth2_scheme)]
