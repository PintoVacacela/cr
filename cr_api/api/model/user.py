from .model import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from marshmallow.fields import Nested
import enum



class UserState(enum.Enum):
    ACTIVO = 1
    INACTIVO = 2
    REGISTRADO = 3

class TypeState(enum.Enum):
    ACTIVO = 1
    INACTIVO = 2

class ApplicationUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    lastname = db.Column(db.String(100))     
    documentType_id = db.Column(db.Integer, db.ForeignKey("document_type.id"))
    documentType = db.relationship("DocumentType", back_populates="users")
    identification = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    userState = db.Column(db.Enum(UserState), default='REGISTRADO')
    userType_id = db.Column(db.Integer, db.ForeignKey("user_type.id"))
    userType = db.relationship("UserType", back_populates="users")


class UserType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50))
    state = db.Column(db.Enum(TypeState), default='ACTIVO')
    users = db.relationship('ApplicationUser')

class DocumentType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    state = db.Column(db.Enum(TypeState), default='ACTIVO')
    users = db.relationship('ApplicationUser')


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}


class UserTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserType
        include_relationships = True
        load_instance = True

class DocumentTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DocumentType
        include_relationships = True
        load_instance = True


class UserSchema(SQLAlchemyAutoSchema):
    DocumentType = Nested(DocumentTypeSchema)
    userState = EnumADiccionario(attribute=("userState"))
    userType = Nested(UserTypeSchema)

    class Meta:
        model = ApplicationUser
        include_relationships = True
        load_instance = True
