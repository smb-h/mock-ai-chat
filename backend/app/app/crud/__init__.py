from .crud_interaction import interaction  # noqa
from .crud_msg import msg  # noqa
from .crud_user import user  # noqa

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
