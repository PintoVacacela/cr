
from . import db
from .model import *


class ClientType(Enum):
    N = "Natural"
    J = "Juridica"
    I = "SinId"
    P = "Placa"

class PaymentType(Enum):
    Contado = False
    Credito = True

class Client(BasicModel):
    id_client=db.Column(db.String(16))
    ruc=db.Column(db.String(13))
    cedula=db.Column(db.String(10))
    placa=db.Column(db.String(13))
    razon_social=db.Column(db.String(300))
    telefonos=db.Column(db.String(50))
    direccion=db.Column(db.String(300))
    tipo=db.Column(db.String(10))
    es_cliente=db.Column(db.Boolean)
    es_proveedor=db.Column(db.Boolean)
    es_empleado=db.Column(db.Boolean)
    es_corporativo=db.Column(db.Boolean)
    aplicar_cupo=db.Column(db.Boolean)
    email=db.Column(db.String(300))
    es_vendedor=db.Column(db.Boolean)
    es_extranjero=db.Column(db.Boolean)
    porcentaje_descuento=db.Column(db.Float) 
    adicional1_cliente=db.Column(db.String(300))
    adicional2_cliente=db.Column(db.String(300))
    adicional3_cliente=db.Column(db.String(300))
    adicional4_cliente=db.Column(db.String(300))
    adicional1_proveedor=db.Column(db.String(300))
    adicional2_proveedor=db.Column(db.String(300))
    adicional3_proveedor=db.Column(db.String(300))
    adicional4_proveedor=db.Column(db.String(300))
    banco_codigo_id=db.Column(db.String(16))
    tipo_cuenta=db.Column(db.String(2))
    numero_tarjeta=db.Column(db.String(200))
    personaasociada_id=db.Column(db.String(16))
    nombre_comercial=db.Column(db.String(300))
    origen=db.Column(db.String(3))
    pvp_default=db.Column(db.String(50))
    id_categoria=db.Column(db.String(16))
    categoria_nombre=db.Column(db.String(40))
    contacts = db.relationship('ContactInfo', back_populates='client')
    addresses = db.relationship('DeliveryAddress', back_populates='client')
    payment_method = db.relationship("PaymentMethod", back_populates="client")

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
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), unique=True)
    client = db.relationship("Client", back_populates="payment_method")
    
    

