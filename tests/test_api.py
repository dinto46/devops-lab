import os
import httpx

BASE_URL = os.getenv(
	"TEST_BASE_URL",
	"http://127.0.0.1:8000"
)

def test_get_tasks():
	response = httpx.get(
		f"{BASE_URL}/tasks",
		timeout=10
	)
	assert response.status_code == 200
	assert isinstance(response.json(),list)


def test_create_task():
	payload = {
		"title": "Pytest API Test",
		"description": "Verify task creation through the API"
	}

	response = httpx.post(
		f"{BASE_URL}/tasks",
		json=payload,
		timeout=10
	)

	assert response.status_code == 200,response.text

	data = response.json()
	assert data["title"] == payload["title"]
	assert data["description"] == payload["description"]
	assert "id" in data


