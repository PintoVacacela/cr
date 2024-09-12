from ..logic.ModelManager import *
from ...model.user import *
from sqlalchemy import create_engine, Column, Integer, String, or_


class UserManager (ModelManager):

    def __init__(self):
        super().__init__(ApplicationUser)

    def findRegisteredUser(self,username,email,identification):
        try:
            search = self.model.query.filter(
            or_(self.model.username == username, 
                self.model.email == email,
                self.model.identification == identification
                )
            ).first()
            return search
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        
    
    def findUserByUserName(self,username):
        try:
            search = self.model.query.filter(self.model.username == username).first()
            return search
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
