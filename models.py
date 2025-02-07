from database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    title = Column(String(length=55),nullable=False,index=True)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean,default=False)
    owner_id = Column(Integer,ForeignKey("users.id"))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    first_name = Column(String(length=55),nullable=False,index=True)
    last_name = Column(String(length=55),nullable=False,index=True)
    age = Column(Integer)
    email = Column(String(length=93),unique=True)
    username = Column(String(length=93),nullable=False,unique=True)
    role = Column(String(length=33),nullable=False,default="user")
    password = Column(String(length=255))