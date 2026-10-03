import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.model import get_sentiment_model


class FakeModel:
    def predict(self, text):
        return {"sentiment": "positive", "confidence": 0.9876}


@pytest.fixture(autouse=True)
def fake_model(monkeypatch):
    monkeypatch.setattr("app.main.get_sentiment_model", lambda: FakeModel())


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_analyze(client):
    response = client.post("/api/analyze", json={"text": "I love this product!"})
    assert response.status_code == 200
    assert response.json() == {"sentiment": "positive", "confidence": 0.9876}


def test_analyze_rejects_empty_text(client):
    response = client.post("/api/analyze", json={"text": "   "})
    assert response.status_code == 422


def test_analyze_rejects_more_than_500_words(client):
    text = " ".join(["word"] * 501)
    response = client.post("/api/analyze", json={"text": text})
    assert response.status_code == 422


def test_batch(client):
    response = client.post(
        "/api/analyze/batch",
        json={"texts": ["Great service", "This is bad", "It is a product"]},
    )
    assert response.status_code == 200
    assert len(response.json()["results"]) == 3


def test_batch_rejects_more_than_10(client):
    response = client.post(
        "/api/analyze/batch",
        json={"texts": ["hello"] * 11},
    )
    assert response.status_code == 422
