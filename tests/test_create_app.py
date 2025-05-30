import pytest
from flask import Flask
from prebuilt.app import create_app

@pytest.fixture
def app():
    app = create_app("microsoft/DialoGPT-medium")
    app.config.update({"TESTING": True})
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_app_returns_flask_instance(app):
    assert isinstance(app, Flask)

def test_model_is_loaded_into_state(app):
    state = app.config.get("state")
    assert state is not None
    assert "tokenizer" in state
    assert "model" in state
    assert "device" in state
    assert "chat_history_ids" in state

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Chatbot" in response.data or b"<html" in response.data  # adjust if needed

def test_chat_route_with_missing_message(client):
    response = client.post("/chat", json={})
    assert response.status_code == 400
    assert "error" in response.json
