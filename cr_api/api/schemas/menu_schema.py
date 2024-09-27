from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested
from ..model.menu import *

class MenuSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    class Meta:
        model = ApplicationMenu
        include_relationships = True
        load_instance = True