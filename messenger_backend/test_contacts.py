from fastapi.testclient import TestClient

from server import app, db

client = TestClient(app)


def test_search_works():
    login1, password1 = "test1", "test1"
    login2, password2 = "test2", "test2"

    db.delete("user:" + login1)
    db.delete("user:" + login2)

    client.get(
        "/signup",
        params={
            "login": login1,
            "password1": password1,
            "password2": password1,
        },
    )
    client.get(
        "/signup",
        params={
            "login": login2,
            "password1": password2,
            "password2": password2,
        },
    )

    auth_res = client.get(
        "/signin",
        params={
            "login": login1,
            "password": password1,
        },
    )

    res = client.get(
        "/search", params={"prefix": "test"}, headers={"session-id": auth_res.json()}
    )

    assert res.status_code == 200
    assert len(res.json()) == 2
    assert login1 in res.json()
    assert login2 in res.json()


def test_new_contact_can_be_added_and_removed():
    login1, password1 = "test1", "test1"
    login2, password2 = "test2", "test2"

    db.delete("user:" + login1)
    db.delete("user:" + login2)

    client.get(
        "/signup",
        params={
            "login": login1,
            "password1": password1,
            "password2": password1,
        },
    )
    client.get(
        "/signup",
        params={
            "login": login2,
            "password1": password2,
            "password2": password2,
        },
    )

    auth_res = client.get(
        "/signin",
        params={
            "login": login1,
            "password": password1,
        },
    )

    session_id = auth_res.json()

    res = client.post(
        "/contacts",
        json={"contact_id": login2},
        headers={"session-id": session_id},
    )

    assert res.status_code == 200

    res2 = client.get("/contacts", headers={"session-id": session_id})
    assert len(res2.json()) == 1

    res3 = client.post(
        "/contacts/delete",
        headers={"session-id": session_id},
        json={"contact_id": login2}
    )

    assert res3.status_code == 200

    res4 = client.get("/contacts", headers={"session-id": session_id})
    assert len(res4.json()) == 0
