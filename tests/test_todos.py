from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from general import get_db

from database import Base
from main import app

client = TestClient(app)


DATABASE_URL = "sqlite:///./testdb.db"
engine = create_engine(
	DATABASE_URL,
	connect_args={"check_same_thread": False},
	poolclass=StaticPool
)

Base.metadata.create_all(engine)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db():
	db = TestingSessionLocal()
	try:
		yield db
	finally:
		db.close()

app.dependency_overrides[get_db] = override_get_db

def test_all_todo_list():
	token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJrZXRtb24iLCJleHAiOjE3Mzg5MzYzMTB9.iGFlNMp6LSJY_2DTMBXIWJroWiltJdB95Xl9kWwAM50"
	response = client.get("todo/list",headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200
	assert response.json() == []
