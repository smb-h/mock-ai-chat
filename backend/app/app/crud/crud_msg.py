import hashlib
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.msg import Msg
from app.schemas.msg import MsgCreate, MsgUpdate


class CRUDMsg(CRUDBase[Msg, MsgCreate, MsgUpdate]):
    def create(
        self, db: Session, *, obj_in: MsgCreate, interaction_id: str
    ) -> Msg:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, interaction_id=interaction_id)
        db_obj.created_at = datetime.now()
        db_obj.updated_at = datetime.now()
        db_obj.id = hashlib.sha256(
            (
                f"{db_obj.id}{db_obj.content}{db_obj.role}"
                + f"{db_obj.interaction_id}"
                + f"{db_obj.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                + f"{db_obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
            ).encode()
        ).hexdigest()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self,
        db: Session,
        *,
        interaction_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Msg]:
        return (
            db.query(self.model)
            .filter(Msg.interaction_id == interaction_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


msg = CRUDMsg(Msg)
