import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

def test_streaming_endpoint(client):
    response = client.get("/streaming_data")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/x-ndjson"  # Adjust based on actual content type

    # Read and verify streamed data
    streamed_data = list(response.iter_lines())
    assert len(streamed_data) > 0
    assert "expected_data" in streamed_data[0]  # Adjust based on your data
