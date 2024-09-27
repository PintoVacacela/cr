
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested
from ..model.model import *
from ..model.user import *
from ..schemas.profile_schema import *

class UserTypeSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    class Meta:
        model = UserType
        include_relationships = True
        load_instance = True
        exclude = ['users']

class DocumentTypeSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    class Meta:
        model = DocumentType
        include_relationships = True
        load_instance = True
        exclude = ['users']


class UserSchema(SQLAlchemyAutoSchema):
    documentType = Nested(DocumentTypeSchema)
    state = EnumADiccionario(attribute=("state"))
    userState = EnumADiccionario(attribute=("userState"))
    userType = Nested(UserTypeSchema)
    profile = Nested(ProfileCompressedSchema)
    class Meta:
        model = ApplicationUser
        include_relationships = True
        load_instance = True
        exclude = ['password']
        
