# tests/test_main.py
from fastapi.testclient import TestClient
import hashlib
from main import app

client = TestClient(app)


def test_welcome():
    r = client.get("/")
    assert r.status_code == 200
    assert "Welcome" in r.json().get("message", "")


def test_checksum():
    payload = {"text": "hello"}
    r = client.post("/checksum", json=payload)
    assert r.status_code == 200
    expected = hashlib.md5(payload["text"].encode("utf-8")).hexdigest()
    assert r.json().get("checksum") == expected


def test_tokens():
    payload = {"text": "hello"}
    r = client.post("/tokens", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "tokens" in data and isinstance(data["tokens"], list)
    assert data.get("checksum") == hashlib.md5(payload["text"].encode("utf-8")).hexdigest()
    assert len(data["tokens"]) == 5
