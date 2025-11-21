from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_analyze_post_contract():
    response = client.post("/analyze", json={"url": "https://github.com/test/repo"})
    assert response.status_code == 202
    assert "task_id" in response.json()
