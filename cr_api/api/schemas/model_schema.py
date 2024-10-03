
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested
from marshmallow import fields
from ..model.model import *
from ..model.user import *
from ..model.client import*
from ..model.profile import*
from ..model.menu import*

class MenuSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    class Meta:
        model = ApplicationMenu
        include_relationships = True
        load_instance = True
        exclude = ['profiles']

class ContactInfoSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    class Meta:
        model = ContactInfo
        include_relationships = True
        load_instance = True

class DeliveryAddressSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    class Meta:
        model = DeliveryAddress
        include_relationships = True
        load_instance = True


class ClientSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    contacts = fields.List(fields.Nested(lambda: ContactInfoSchema()))
    addresses = fields.List(fields.Nested(lambda: DeliveryAddressSchema()))
    class Meta:
        model = Client
        include_relationships = True
        load_instance = True

class UserTypeSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    class Meta:
        model = UserType
        include_relationships = True
        load_instance = True
        exclude = ['users','profiles']

class DocumentTypeSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    class Meta:
        model = DocumentType
        include_relationships = True
        load_instance = True
        exclude = ['users']

class ProfileSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    menus = MenuSchema(many=True) 
    userTypes = UserTypeSchema(many=True) 
    class Meta:
        model = Profile
        include_relationships = True
        load_instance = True
        exclude = ['users']


class ProfileCompressedSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    class Meta:
        model = Profile
        include_relationships = False
        load_instance = True


class UserSchema(SQLAlchemyAutoSchema):
    documentType = Nested(DocumentTypeSchema)
    state = EnumADiccionario(attribute=("state"))
    userState = EnumADiccionario(attribute=("userState"))
    userType = Nested(UserTypeSchema)
    profile =  Nested(ProfileSchema)
    class Meta:
        model = ApplicationUser
        include_relationships = True
        load_instance = True
        exclude = ['password']
        
