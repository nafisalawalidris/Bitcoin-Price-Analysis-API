#  Testing with Pytest for the API endpoints

# test_main.py

import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.main import app  # Import your FastAPI application

# Fixture to provide an HTTP client for testing
@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Test the endpoint to get all prices
@pytest.mark.asyncio
async def test_get_all_prices(client):
    response = await client.get("/prices/")
    assert response.status_code == 200
    assert "prices" in response.json()
    # Add more assertions based on your expected response

# Test the endpoint to get prices by year
@pytest.mark.asyncio
async def test_get_prices_by_year(client):
    year = 2023
    response = await client.get(f"/prices/{year}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Ensure response is a list
    # Add more assertions to check data contents

# Test the endpoint to get prices by halving period
@pytest.mark.asyncio
async def test_get_prices_by_halving(client):
    halving_number = 3
    response = await client.get(f"/prices/halving/{halving_number}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Ensure response is a list
    # Add more assertions to check data contents

# Test the endpoint to get prices across all halvings
@pytest.mark.asyncio
async def test_get_prices_across_halvings(client):
    response = await client.get("/prices/halvings")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Ensure response is a list
    # Add more assertions to check data contents

# Test for 404 response when accessing a non-existent endpoint
@pytest.mark.asyncio
async def test_get_non_existent_endpoint(client):
    response = await client.get("/non-existent-endpoint")
    assert response.status_code == 404
