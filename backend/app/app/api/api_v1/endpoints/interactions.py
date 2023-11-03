from typing import Any

import g4f
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

g4f.debug.logging = True  # enable logging
g4f.check_version = False  # Disable automatic version checking


@router.get("/", response_model=list[schemas.Interaction])
def read_interactions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve interactions.
    """
    if crud.user.is_superuser(current_user):
        interactions = crud.interaction.get_multi(db, skip=skip, limit=limit)
    else:
        interactions = crud.interaction.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return interactions


@router.post("/", response_model=schemas.Interaction)
def create_interaction(
    *,
    db: Session = Depends(deps.get_db),
    interaction_in: schemas.InteractionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new interaction.
    """
    interaction = crud.interaction.create_with_owner(
        db=db, obj_in=interaction_in, owner_id=current_user.id
    )
    # AI
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[
            {"role": interaction_in.role, "content": interaction_in.prompt}
        ],
    )
    crud.msg.create(
        db=db,
        obj_in=schemas.MsgCreate(role="AI", content=response),
        interaction_id=interaction.id,
    )

    return interaction


# @router.put("/{id}", response_model=schemas.Interaction)
# def update_interaction(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: str,
#     interaction_in: schemas.InteractionUpdate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update an interaction.
#     """
#     interaction = crud.interaction.get(db=db, id=id)
#     if not interaction:
#         raise HTTPException(status_code=404, detail="Interaction not found")
#     if not crud.user.is_superuser(current_user) and (
#         interaction.owner_id != current_user.id
#     ):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     interaction = crud.interaction.update(
#         db=db, db_obj=interaction, obj_in=interaction_in
#     )
#     return interaction


# Create interaction message
@router.post("/{id}/messages/", response_model=schemas.Msg)
def create_interaction_message(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    message_in: schemas.MsgCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new message for an interaction.
    """
    interaction = crud.interaction.get(db=db, id=id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    if not crud.user.is_superuser(current_user) and (
        interaction.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    message = crud.msg.create(
        db=db, obj_in=message_in, interaction_id=interaction.id
    )
    # AI
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": message_in.role, "content": message_in.content}],
    )
    crud.msg.create(
        db=db,
        obj_in=schemas.MsgCreate(role="AI", content=response),
        interaction_id=interaction.id,
    )
    return message


@router.get("/{id}", response_model=schemas.Interaction)
def read_interaction(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get interaction by ID.
    """
    interaction = crud.interaction.get(db=db, id=id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    if not crud.user.is_superuser(current_user) and (
        interaction.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return interaction


@router.delete("/{id}", response_model=schemas.Interaction)
def delete_interaction(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an interaction.
    """
    interaction = crud.interaction.get(db=db, id=id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    if not crud.user.is_superuser(current_user) and (
        interaction.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    for msg in interaction.msgs:
        crud.msg.remove(db=db, id=msg.id)
    interaction = crud.interaction.remove(db=db, id=id)
    return interaction
