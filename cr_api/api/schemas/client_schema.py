from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested
from ..model.client import *


class ClientSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    tipo = EnumADiccionario(attribute=("tipo"))
    class Meta:
        model = Client
        include_relationships = True
        load_instance = True