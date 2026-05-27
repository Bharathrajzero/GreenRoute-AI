import pytest
from fastapi.testclient import TestClient
from src.main import app

# Initialize test fixture loop
client = TestClient(app)

# Explicit startup hook activation for testing runtime
app.router.startup()

def test_system_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_simple_routing_logic():
    payload = {"prompt": "What is 2 + 2?"}
    response = client.post("/v1/chat/completions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["complexity_tier"] == "SIMPLE"
    assert data["route"] == "Local-SLM"

def test_complex_routing_logic():
    payload = {"prompt": "Architect and optimize a compilation engine to evaluate and benchmark real-time system pipelines."}
    response = client.post("/v1/chat/completions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["complexity_tier"] == "COMPLEX"
    assert data["route"] == "Cloud-LLM"
