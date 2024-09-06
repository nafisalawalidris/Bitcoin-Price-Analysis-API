from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@patch("app.realtime_service.get_real_time_data")
def test_mocked_realtime_data(mock_get_real_time_data, client):
    mock_get_real_time_data.return_value = {"data": "mocked data"}
    
    response = client.get("/realtime_data")
    assert response.status_code == 200
    assert response.json() == {"data": "mocked data"}
