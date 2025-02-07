from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_main():
	response = client.get("/ketmon")
	assert response.status_code == 200
	assert response.json() == {"success": True}
