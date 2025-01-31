# pip install sqlalchemy
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_USER,DATABASE_PORT,DATABASE_HOST,DATABASE_NAME,DATABASE_PASSWORD
# DATABSE_SQLITE_URL = "sqlite:///./todos.db"
# engine = create_engine(DATABSE_SQLITE_URL,connect_args={"check_same_thread": False})

DATABSE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

engine = create_engine(DATABSE_URL)
SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base = declarative_base()