from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Interaction(Base):
    id = Column(String, primary_key=True, index=True)
    prompt = Column(String)
    agent = Column(String)
    role = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="interactions")
    msgs = relationship("Msg", back_populates="interaction")
    created_at = Column(String)
    updated_at = Column(String)
