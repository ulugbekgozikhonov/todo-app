# pip install sqlalchemy
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DATABSE_SQLITE_URL = "sqlite:///./todos.db"
# engine = create_engine(DATABSE_SQLITE_URL,connect_args={"check_same_thread": False})

DATABSE_POSTGRESQL_URL = "postgresql://postgres:root_123@localhost/dangasalar1905"

engine = create_engine(DATABSE_POSTGRESQL_URL)
SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base = declarative_base()