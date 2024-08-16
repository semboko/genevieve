from fastapi.testclient import TestClient

from server import app, db
from tests.utils import create_test_user

client = TestClient(app)


def test_send_message():
    u1 = create_test_user()
    u2 = create_test_user()
    res = client.post("/contacts", json={
        "contact_id": u2.login
    }, headers={
        "session-id": u1.token
    })
    assert res.status_code == 200
    res = client.post("/message", json={
        "content": "whatever",
        "contact_id": u2.login,
    }, headers={
        "session-id": u1.token
    })
    res.status_code == 200
    res = client.get(
        "/message",
        params={"contact_id": u2.login, "start": 0, "end": 10},
        headers={"session-id": u1.token},
    )
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_get_empty_chat():
    u1 = create_test_user()
    u2 = create_test_user()
    res = client.get(
        "/message",
        params={"contact_id": u2.login, "start": 0, "end": 10},
        headers={"session-id": u1.token}
    )
    assert res.status_code == 200
    assert len(res.json()) == 0
