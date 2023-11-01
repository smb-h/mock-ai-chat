from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Interaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, index=True)
    model_name = Column(String)
    role = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="interactions")
    created_at = Column(String)
    updated_at = Column(String)
