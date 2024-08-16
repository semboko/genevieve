from pydantic import BaseModel


class AddContactRequest(BaseModel):
    contact_id: str


class RemoveContactRequest(BaseModel):
    contact_id: str


class MessageRequest(BaseModel):
    contact_id: str
    content: str
