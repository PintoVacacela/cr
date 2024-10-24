
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,auto_field
from marshmallow.fields import Nested
from marshmallow import fields
from ..model.model import *
from ..model.user import *
from ..model.client import*
from ..model.profile import*
from ..model.product import *
from ..model.menu import*
from ..model.notification import * 
from ..model.client_service import *

class ServiceSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    class Meta:
        model = Service
        include_relationships = True
        load_instance = True


class ProductSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    product_type = EnumADiccionario(attribute=("product_type"))
    type = EnumADiccionario(attribute=("type"))
    class Meta:
        model = Product
        include_relationships = True
        load_instance = True

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

class PaymentMethodSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    type = EnumADiccionario(attribute=("type"))
    class Meta:
        model = PaymentMethod
        include_relationships = True
        load_instance = True

class ClientCategorySchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    class Meta:
        model = ClientCategory
        include_relationships = True
        load_instance = True

class ClientSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    type = EnumADiccionario(attribute=("type"))
    contacts = fields.List(fields.Nested(lambda: ContactInfoSchema()))
    addresses = fields.List(fields.Nested(lambda: DeliveryAddressSchema()))
    category = Nested(ClientCategorySchema)
    payment_method = fields.Nested(PaymentMethodSchema)
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


class EventDaySchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    day = EnumADiccionario(attribute=("day"))
    class Meta:
        model = EventDay
        include_relationships = False
        load_instance = True

class EventCompressedSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    type = EnumADiccionario(attribute=("type"))
    frequency_type = EnumADiccionario(attribute=("frequency_type"))
    client =  Nested(ClientSchema)
    class Meta:
        model = Event
        include_relationships = True
        load_instance = True


class UserSchema(SQLAlchemyAutoSchema):
    documentType = Nested(DocumentTypeSchema)
    state = EnumADiccionario(attribute=("state"))
    userState = EnumADiccionario(attribute=("userState"))
    userType = Nested(UserTypeSchema)
    profile =  Nested(ProfileSchema) 
    events = EventCompressedSchema(many=True) 
    class Meta:
        model = ApplicationUser
        include_relationships = True
        load_instance = True
        exclude = ['password']

class EventSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    type = EnumADiccionario(attribute=("type"))
    frequency_type = EnumADiccionario(attribute=("frequency_type"))
    days = fields.List(fields.Nested(lambda: EventDaySchema()))
    client =  Nested(ClientSchema)
    users = fields.List(fields.Nested(lambda: UserSchema()))
    services = fields.List(fields.Nested(lambda: ServiceSchema()))
    class Meta:
        model = Event
        include_relationships = True
        load_instance = True

class ScheduledEventSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    event =  Nested(EventCompressedSchema)
    class Meta:
        model = ScheduledEvent
        include_relationships = False
        load_instance = True
        

class UserNotificationSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    type = EnumADiccionario(attribute=("type"))
    class Meta:
        model = UserNotification
        include_relationships = True
        load_instance = True



