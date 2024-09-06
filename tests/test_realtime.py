import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

def test_websocket_connection(client):
    with client.websocket_connect("/ws/updates") as websocket:
        websocket.send_text("Request update")
        response = websocket.receive_text()
        assert response == "Update received"  # Adjust based on expected response
