# from typing import Optional
from datetime import datetime

from pydantic import BaseModel, field_serializer


# Shared properties
class InteractionBase(BaseModel):
    prompt: str | None = None
    agent: str | None = None
    role: str | None = None


# Properties to receive on Interaction creation
class InteractionCreate(InteractionBase):
    prompt: str
    agent: str
    role: str


# Properties to receive on Interaction update
class InteractionUpdate(InteractionBase):
    pass


# Properties shared by models stored in DB
class InteractionInDBBase(InteractionBase):
    id: str
    prompt: str
    owner_id: int
    agent: str
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Properties to return to client
class Interaction(InteractionInDBBase):
    messages: list[dict] = []
    settings: dict = {}

    @field_serializer("settings")
    def serialize_settings(self, v):
        return {}


# Properties properties stored in DB
class InteractionInDB(InteractionInDBBase):
    pass
