from fastapi.testclient import TestClient
from typing import Optional
from secrets import token_hex
from pydantic import BaseModel

from server import app, db

client = TestClient(app)


class TestUser(BaseModel):
    login: str
    token: str


def create_test_user(
    login: Optional[str] = None,
    password: Optional[str] = None,
) -> TestUser:
    login = login or "test" + token_hex(32)
    password = password or login

    db.delete("user:" + login)
    client.get(
        "/signup",
        params={
            "login": login,
            "password1": password,
            "password2": password,
        },
    )
    auth_res = client.get(
        "/signin",
        params={
            "login": login,
            "password": password,
        },
    )

    return TestUser(token=auth_res.json(), login=login)
