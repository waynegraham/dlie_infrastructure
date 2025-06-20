"""
Basic smoke tests for the FastAPI application.
"""
import os
import sys

# Ensure the repository root is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi.testclient import TestClient
import pytest

from api.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_openapi_schema(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "paths" in data
    assert "/resources" in data["paths"]


def test_swagger_ui(client):
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Swagger UI" in response.text
