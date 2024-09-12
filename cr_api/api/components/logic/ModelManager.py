from ...model import db
from ...utilities.responses import *


response_util = WebResponse()

class ModelManager:

    def __init__(self, model):
        self.model = model
        self.log = LoggerFactory().get_logger(self.__class__)

    def create(self,new_object):
        try:
            db.session.add(new_object)
            db.session.commit()
            return True
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return False

    def put(self):
        try:
            db.session.commit()
            return True
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return False

    def delete(self,object):
        try:
            db.session.delete(object)
            db.session.commit()
            return True
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return False
        
    def findAll(self):
        try:
            return self.model.query.all()
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        
    def findById(self,id_object):
        try:
            return self.model.query.filter(self.model.id == id_object).first()
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None