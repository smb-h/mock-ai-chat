from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .interaction import Interaction  # noqa: F401


class Msg(Base):
    id = Column(String, primary_key=True, index=True)
    interaction_id = Column(String, ForeignKey("interaction.id"))
    interaction = relationship("Interaction", back_populates="msgs")
    role = Column(String)
    content = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
