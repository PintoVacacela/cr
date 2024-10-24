
from . import db
from enum import Enum
from .model import *

class ProductType(Enum):
    PRO = "Producto"
    SER = "Servicio"

class ProductSubType(Enum):
    SIM = "Simple"
    COM = "Combo" 
    COP = "Compuesto" 
    PRO = "Produccion"

class Product(BasicModel):
    id_product = db.Column(db.String(100))
    code = db.Column(db.String(200)) 
    product_type = db.Column(db.Enum(ProductSubType), default='SIM')
    for_pos = db.Column(db.Boolean) 
    name = db.Column(db.String(300))  
    barcode = db.Column(db.String(50))  
    category_id = db.Column(db.String(16))  
    brand_id = db.Column(db.String(16)) 
    brand_name = db.Column(db.String(50))  
    vat_percentage = db.Column(db.Integer) 
    pvp1 = db.Column(db.Float)  
    pvp2 = db.Column(db.Float)  
    pvp3 = db.Column(db.Float)  
    pvp4 = db.Column(db.Float)  
    minimum = db.Column(db.Float)  
    stock_quantity = db.Column(db.String(16))  
    manual_pvp = db.Column(db.Boolean)  
    image = db.Column(db.String(300)) 
    description = db.Column(db.String(100))  
    type = db.Column(db.Enum(ProductType), default='PRO') 
    max_cost = db.Column(db.Float) 
    creation_date = db.Column(db.String(16))  
    supplier_code = db.Column(db.String(200))  
    lead_time = db.Column(db.Integer)  
    automatic_generation = db.Column(db.Boolean)
