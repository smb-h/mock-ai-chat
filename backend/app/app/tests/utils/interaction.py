# from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.interaction import InteractionCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_interaction(
    db: Session, *, owner_id: int | None = None
) -> models.Interaction:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    interaction_in = InteractionCreate(
        title=title, description=description, id=id
    )
    return crud.interaction.create_with_owner(
        db=db, obj_in=interaction_in, owner_id=owner_id
    )
