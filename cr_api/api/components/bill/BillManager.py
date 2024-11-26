from ..logic.ModelManager import *
from ...model.bill import *
from sqlalchemy.orm import aliased
import requests


class BillManager (ModelManager):

    def __init__(self):
        super().__init__(Bill)

    def findClientBills(self,client_id):
        try:
            search = self.model.query.filter(self.model.client_id == client_id).all()
            return search
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
       
    def appendDetails(self,bill_id,products):
        print(bill_id)
        try:
            BillDetail.query.filter(BillDetail.bill_id==bill_id).delete()
            db.session.commit()
            for item in products:
                new_item = BillDetail(
                    bill_id = bill_id,
                    product_id = item.get("productId"),
                    price = item.get("price"),
                    quantity = item.get("quantity"),
                    iva = item.get("iva"),
                    discount = item.get("discount"),
                    discountTotal = item.get("discountTotal"),
                    subtotal = item.get("subtotal"),
                    total = item.get("total")
                )
                db.session.add(new_item)
            db.session.commit()
            return True
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        

        
    
        
   
    