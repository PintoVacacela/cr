from ..logic.ModelManager import *
from ...model.product import *
from ...model.client_service import *
from ...model.client import *
from sqlalchemy.orm import aliased
import requests


class AssigmentManager ():

    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        Session = sessionmaker()
        self.session = Session()
       
    def appendProducts(self,client_id,products):
        try:
            ProductAssignment.query.filter(ProductAssignment.client_id==client_id).delete()
            db.session.commit()
            for item in products:
                new_item = ProductAssignment(
                    client_id = client_id,
                    product_id = int(item.get("id")),
                    value = item.get("value")
                )
                db.session.add(new_item)
                db.session.commit()
            return True
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        
    
        
    def findClientsAssignments(self):
        try:

            clients_with_assignments = db.session.query(Client).join(ProductAssignment, Client.id == ProductAssignment.client_id, isouter=True) \
                .filter(
                        ProductAssignment.client_id.isnot(None),
                ).distinct().all()
            return clients_with_assignments
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        
    def deleteAssignments(self,client_id):
        try:
            ProductAssignment.query.filter(ProductAssignment.client_id==client_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        
    

    def findProductAssingments(self,client_id):
        try:
            return ProductAssignment.query.filter(ProductAssignment.client_id == client_id).all()
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        

        
    

    
        
    




    