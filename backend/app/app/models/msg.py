from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .interaction import Interaction  # noqa: F401


class Msg(Base):
    id = Column(Integer, primary_key=True, index=True)
    interaction = relationship("Interaction", back_populates="msgs")
    interaction_id = Column(Integer, ForeignKey("interaction.id"))
    created_at = Column(String)
    role = Column(String)
    content = Column(String)
