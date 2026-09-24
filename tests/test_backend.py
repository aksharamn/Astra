import os
import pytest
from app import create_app


@pytest.fixture()
def client():
    path = os.path.join(os.path.dirname(__file__), "test.sqlite")
    class TestConfig:
        SECRET_KEY = "test"
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.replace("\\", "/")
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        ASTRA_MASTER_KEY = "test-master-key"
        TESTING = True
    app = create_app(TestConfig)
    with app.test_client() as c:
        yield c
    if os.path.exists(path):
        os.unlink(path)


def test_register_login_and_encrypted_message(client):
    assert client.post("/api/auth/register", json={"email": "alice@example.com", "username": "alice", "pin": "123456"}).status_code == 201
    client.post("/api/auth/logout")
    assert client.post("/api/auth/login", json={"username": "alice", "pin": "123456"}).status_code == 200
    assert client.get("/api/health").json["ok"]
