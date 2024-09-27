
from . import db
from .model import *


class Type(Enum):
    N = "Natural"
    J = "Juridica"
    I = "SinId"
    P = "Placa"

class Client(BasicModel):
    id_client=db.Column(db.String(16))
    ruc=db.Column(db.String(13))
    cedula=db.Column(db.String(10), nullable=False)
    placa=db.Column(db.String(13))
    razon_social=db.Column(db.String(300), nullable=False)
    telefonos=db.Column(db.String(50))
    direccion=db.Column(db.String(300))
    tipo=db.Column(db.Enum(Type), default='N', nullable=False)
    es_cliente=db.Column(db.Boolean, nullable=False)
    es_proveedor=db.Column(db.Boolean, nullable=False)
    es_empleado=db.Column(db.Boolean)
    es_corporativo=db.Column(db.Boolean)
    aplicar_cupo=db.Column(db.Boolean)
    email=db.Column(db.String(300))
    es_vendedor=db.Column(db.Boolean)
    es_extranjero=db.Column(db.Boolean)
    porcentaje_descuento=db.Column(db.Numeric(10, 2)) 
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

