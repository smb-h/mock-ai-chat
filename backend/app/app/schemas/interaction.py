# from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field

from .msg import Msg


# Shared properties
class InteractionBase(BaseModel):
    prompt: str
    agent: str
    role: str


# Properties to receive on Interaction creation
class InteractionCreate(InteractionBase):
    pass


# Properties to receive on Interaction update
class InteractionUpdate(InteractionBase):
    pass


# Properties shared by models stored in DB
class InteractionInDBBase(InteractionBase):
    id: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Properties to return to client
class Interaction(InteractionInDBBase):
    # prompt: str = Field(..., exclude=True)
    agent: str = Field(..., serialization_alias="model_name")
    # role: str = Field(..., exclude=True)
    owner_id: int = Field(..., exclude=True)
    msgs: list[Msg] = Field(default=[], serialization_alias="messages")

    # @property
    # def settings(self):
    #     return {
    #         "prompt": self.prompt,
    #         "agent": self.agent,
    #         "role": self.role,
    #     }

    class Config:
        from_attributes = True


# Properties properties stored in DB
class InteractionInDB(InteractionInDBBase):
    pass
