from datetime import datetime

from pydantic import BaseModel


class Msg(BaseModel):
    id: str
    created_at: datetime
    role: str
    content: str
