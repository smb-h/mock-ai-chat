# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.interaction import Interaction  # noqa
from app.models.msg import Msg  # noqa
from app.models.user import User  # noqa
