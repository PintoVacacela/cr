from ..logic.ModelManager import *
from ...model.client_service import *
from sqlalchemy import or_

class ServiceManager (ModelManager):

    def __init__(self):
        super().__init__(Service)


    def findServiceByCodeAndName(self,name,code):
            try:
                search = self.model.query.filter(
                or_(self.model.name == name, 
                    self.model.code == code
                    )
                ).first()
                return search
            except Exception as e:
                self.log.errorExc(None,e,traceback)
                return None