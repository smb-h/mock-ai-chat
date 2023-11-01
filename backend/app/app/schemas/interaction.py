# from typing import Optional

from pydantic import BaseModel


# Shared properties
class InteractionBase(BaseModel):
    prompt: str | None = None
    model_name: str | None = None
    role: str | None = None


# Properties to receive on Interaction creation
class InteractionCreate(InteractionBase):
    prompt: str
    model_name: str
    role: str


# Properties to receive on Interaction update
class InteractionUpdate(InteractionBase):
    pass


# Properties shared by models stored in DB
class InteractionInDBBase(InteractionBase):
    id: int
    prompt: str
    owner_id: int
    model_name: str
    role: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


# Properties to return to client
class Interaction(InteractionInDBBase):
    pass


# Properties properties stored in DB
class InteractionInDB(InteractionInDBBase):
    pass
