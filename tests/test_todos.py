from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from database import Base
from general import get_db
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


app.dependency_overrides = {get_db: override_get_db}


def test_all_todo_list():
	token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJrZXRtb24iLCJleHAiOjE3MzkxOTE3NTV9.mwgf671cGiLAE4U3hi-eji3F-WPv77Y-MCNpbdrqOP0"
	response = client.get("todo/list", headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200
	assert response.json() == []


def test_todo_by_id():
	token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJrZXRtb24iLCJleHAiOjE3MzkxOTE3NTV9.mwgf671cGiLAE4U3hi-eji3F-WPv77Y-MCNpbdrqOP0"
	response = client.get('todo/1', headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200
	assert len(response.json()) == 1


def test_create_task():
	token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJrZXRtb24iLCJleHAiOjE3MzkxOTE3NTV9.mwgf671cGiLAE4U3hi-eji3F-WPv77Y-MCNpbdrqOP0"
	response = client.post(
		'todo/create',
		headers={"Authorization": f"Bearer {token}"},
		json={
			"title": "Task title",
			"description": "Task description",
			"priority": 5,
			"completed": False,
			"owner_id": 1
		}
	)
	assert response.status_code == 201
	assert response.json() == {}
