from . import db
from .model import *

class BillType(Enum):
    FAC = "Factura"
    LQC = "Liquidacion Compra"

class DocumentState(Enum):
    P = "Pendiente"
    C = "Cobrado"
    G = "Pagado"
    A = "Anulado"
    E = "Generado"
    F = "Facturado"

class Bill(BasicModel):
    issue_date = db.Column(db.Date, nullable=False)
    document_type = db.Column(db.Enum(BillType), default='FAC') 
    document = db.Column(db.String(17), nullable=False)
    document_state = db.Column(db.Enum(DocumentState)) 
    authorization = db.Column(db.String(49))
    box_id = db.Column(db.String(16))
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    client = db.relationship("Client", back_populates="bills")
    description = db.Column(db.String(200))
    subtotal_0 = db.Column(db.Float) 
    subtotal_12 = db.Column(db.Float) 
    iva = db.Column(db.Float) 
    ice = db.Column(db.Float) 
    service = db.Column(db.Float) 
    total = db.Column(db.Float) 
    aditional1 = db.Column(db.String(300))
    aditional2 = db.Column(db.String(300))
    details = db.relationship('BillDetail', back_populates='bill')
    seller_id = db.Column(db.Integer, db.ForeignKey("application_user.id"))
    seller = db.relationship("ApplicationUser", back_populates="bills")
    is_sended = db.Column(db.Boolean, default= False)

class BillDetail(db.Model):
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id') ,primary_key=True)
    bill = db.relationship("Bill", back_populates="details")
    product_id = db.Column(db.Integer, db.ForeignKey('product.id') ,primary_key=True)
    product = db.relationship("Product")
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    iva = db.Column(db.Float)
    discount = db.Column(db.Float)
    discountTotal = db.Column(db.Float)
    subtotal = db.Column(db.Float)
    total = db.Column(db.Float)


    
    
    

    

    