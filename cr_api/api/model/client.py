
from . import db
from .model import *


class ClientType(Enum):
    N = "Natural"
    J = "Juridica"
    I = "SinId"
    # P = "Placa"

class PaymentType(Enum):
    Contado = 1
    Credito = 2

class Client(BasicModel):
    id_client=db.Column(db.String(16))
    type = db.Column(db.Enum(ClientType), default='N')
    ruc = db.Column(db.String(13))
    identification = db.Column(db.String(10),unique=True, nullable=False)
    name = db.Column(db.String(300),nullable=False)
    comercial_name = db.Column(db.String(300))
    province = db.Column(db.String(50))
    canton = db.Column(db.String(50))
    parish = db.Column(db.String(50))
    sex = db.Column(db.String(50))
    civil_state = db.Column(db.String(50))
    source_income = db.Column(db.String(50))
    is_foreign = db.Column(db.Boolean)
    special_taxpayer  = db.Column(db.Boolean)
    email = db.Column(db.String(50))
    default_phone = db.Column(db.String(200))
    default_address = db.Column(db.String(200))
    contacts = db.relationship('ContactInfo', back_populates='client')
    addresses = db.relationship('DeliveryAddress', back_populates='client')
    payment_method = db.relationship("PaymentMethod",uselist=False, back_populates="client", cascade='all, delete-orphan')
    category_id = db.Column(db.Integer, db.ForeignKey("client_category.id"))
    category = db.relationship("ClientCategory", back_populates="clients")
    events = db.relationship('Event')

class ContactInfo(BasicModel):
    area = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    client = db.relationship("Client", back_populates="contacts")
    default = db.Column(db.Boolean)

class DeliveryAddress(BasicModel):
    location = db.Column(db.String(100))
    address = db.Column(db.String(600))
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    client = db.relationship("Client", back_populates="addresses")
    default = db.Column(db.Boolean)

class PaymentMethod(BasicModel):
    type = db.Column(db.Enum(PaymentType), default='Contado')
    days = db.Column(db.Integer)
    max_amount = db.Column(db.Float)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), unique=True)
    client = db.relationship("Client", back_populates="payment_method")


class ClientCategory(BasicModel):
    code = db.Column(db.String(20))
    name = db.Column(db.String(100))
    parent_id = db.Column(db.Integer)
    clients = db.relationship('Client')


    
    

