from fastapi.testclient import TestClient

from server import app, db

client = TestClient(app)


def test_signup_success():
    login, password = "login", "password"
    db.delete("user:" + login)
    res = client.get(
        "/signup", params={"login": login, "password1": password, "password2": password}
    )

    assert res.status_code == 200
    assert res.text == "true"


def test_signup_fail():
    login, password = "login", "password"
    db.delete("user:" + login)
    client.get(
        "/signup", params={"login": login, "password1": password, "password2": password}
    )

    res = client.get(
        "/signup", params={"login": login, "password1": password, "password2": password}
    )

    assert res.status_code == 400


def test_two_passwords_are_not_same():
    login, password = "login", "password"
    db.delete("user:" + login)
    res = client.get(
        "/signup",
        params={"login": login, "password1": password, "password2": "something else"},
    )

    assert res.status_code == 400


def test_signin_success():
    login, password = "login", "password"
    db.delete("user:" + login)
    client.get(
        "/signup",
        params={
            "login": login,
            "password1": password,
            "password2": password,
        },
    )
    res = client.get(
        "/signin",
        params={
            "login": login,
            "password": password,
        },
    )

    assert res.status_code == 200
    assert res.text is not None


def test_signin_fail_user_not_exist():
    res = client.get(
        "/signin",
        params={
            "login": "not-exist",
            "password": "not-exist",
        },
    )
    assert res.status_code == 401


def test_signin_fail_incorrect_password():
    login, password = "login", "password"
    db.delete("user:" + login)
    client.get(
        "/signup",
        params={
            "login": login,
            "password1": password,
            "password2": password,
        },
    )
    res = client.get("/signin", params={"login": login, "password": "not-correct"})

    assert res.status_code == 401
