from hashlib import sha256
from secrets import token_hex
from typing import Annotated, List

from fastapi import FastAPI, Header, HTTPException
from redis import Redis

from schema import AddContactRequest, RemoveContactRequest, MessageRequest
from datetime import datetime, timezone

app = FastAPI()
db = Redis(host="178.62.216.119", port=4567, decode_responses=True)


@app.get(path="/signup")
def signup(login: str, password1: str, password2: str):
    if password2 != password1:
        raise HTTPException(400)

    existing_user = db.get("user:" + login)

    if existing_user is not None:
        raise HTTPException(400)

    hashed_password = sha256(password1.encode("UTF-8")).hexdigest()

    db.set("user:" + login, hashed_password)

    return True


@app.get(path="/signin")
def signin(login: str, password: str):
    expected_hash = db.get("user:" + login)

    if expected_hash is None:
        raise HTTPException(401)

    actual_hash = sha256(password.encode("UTF-8")).hexdigest()

    if expected_hash != actual_hash:
        raise HTTPException(401)

    session_id = token_hex(16)

    db.set("session:" + session_id, login, ex=24 * 60 * 60)

    return session_id


@app.get(path="/search")
def search(prefix: str, session_id: Annotated[str, Header()]):
    username = db.get("session:" + session_id)
    if username is None:
        raise HTTPException(status_code=401)

    users = db.keys("user:" + prefix + "*")
    result = []
    for u in users:
        result.append(u[5:])
    return result


@app.get(path="/contacts")
def get_contacts(session_id: Annotated[str, Header()]) -> List[str]:
    username = db.get("session:" + session_id)
    if username is None:
        raise HTTPException(status_code=401)
    contacts = db.smembers("contacts:" + username)
    return list(sorted(contacts))


@app.post(path="/contacts")
def add_contact(session_id: Annotated[str, Header()], data: AddContactRequest):
    username = db.get("session:" + session_id)
    if username is None:
        raise HTTPException(status_code=401)
    db.sadd("contacts:" + username, data.contact_id)


@app.post(path="/contacts/delete")
def remove_contact(session_id: Annotated[str, Header()], data: RemoveContactRequest):
    username = db.get("session:" + session_id)
    if username is None:
        raise HTTPException(status_code=401)
    db.srem("contacts:" + username, data.contact_id)


@app.post(path="/message")
def send_message(session_id: Annotated[str, Header()], message: MessageRequest):
    username = db.get("session:" + session_id)

    chat_id = db.hget("chats:" + username, message.contact_id)

    if chat_id is None:
        chat_id = token_hex(16)
        db.hset("chats:" + username, message.contact_id, chat_id)
        db.hset("chats:" + message.contact_id, username, chat_id)

    t = datetime.now(timezone.utc).timestamp()

    db.lpush("chat:" + chat_id, f"{username}|{message.content}|{t}")


@app.get(path="/message")
def get_messages(session_id: Annotated[str, Header()], contact_id: str, start: int, end: int):
    username = db.get("session:" + session_id)
    chat_id = db.hget("chats:" + username, contact_id) or "-"
    res = db.lrange("chat:" + chat_id, start, end)
    print(res)
    return res


@app.get(path="/username")
def get_username(session_id: Annotated[str, Header()]) -> str:
    return db.get("session:" + session_id)
