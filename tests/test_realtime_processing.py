import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

def test_realtime_processing(client):
    response = client.post("/process_realtime", json={"data": "sample data"})
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "processed"
    assert "processed_data" in result
