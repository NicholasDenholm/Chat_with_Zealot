import pytest
from prebuilt.app.__init__ import create_app  # assuming you have a create_app() factory

@pytest.fixture
def client():
    model="microsoft/DialoGPT-small"
    app = create_app(model)
    app.config['TESTING'] = True
    app.config['state'] = {"chat_history_ids": []}
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Chatbot" in response.data  # depending on your index.html content

def test_chat_route_missing_message(client):
    response = client.post("/chat", json={})
    assert response.status_code == 400
    assert response.json["error"] == "No message provided"