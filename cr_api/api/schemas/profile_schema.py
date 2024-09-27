from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested
from ..model.profile import *
from .menu_schema import *

class ProfileSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    menus = Nested(MenuSchema)
    class Meta:
        model = Profile
        include_relationships = False
        load_instance = True


class ProfileCompressedSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    class Meta:
        model = Profile
        include_relationships = False
        load_instance = True