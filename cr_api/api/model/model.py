from marshmallow import fields
from enum import Enum
from . import db

class TypeState(Enum):
    ACTIVO = 1
    INACTIVO = 2


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"key": value.name, "value": value.value}
    
class  BasicModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.Enum(TypeState), default='ACTIVO')