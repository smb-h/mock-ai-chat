from datetime import datetime

from pydantic import BaseModel, Field


class MsgBase(BaseModel):
    role: str
    content: str


# Properties to receive on Interaction creation
class MsgCreate(MsgBase):
    pass


class MsgUpdate(MsgBase):
    pass


class MsgInDBBase(MsgBase):
    id: str
    interaction_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Msg(MsgInDBBase):
    updated_at: str = Field(..., exclude=True)
    interaction_id: str = Field(..., exclude=True)


class MsgInDB(MsgInDBBase):
    pass
