from ..logic.ModelManager import *
from ...model.user import *
from sqlalchemy import or_





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
        
    def findRegisteredUserWithoutId(self,id,username,email,identification):
        try:
            search = self.model.query.filter(
            or_(self.model.username == username, 
                self.model.email == email,
                self.model.identification == identification
                ),
                self.model.id != id
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
    
    


    # def findVisualizationUsers(self,id):
    #     try:
    #         search = self.model.query.filter(
    #         or_(self.model.username == username, 
    #             self.model.email == email,
    #             self.model.identification == identification
    #             )
    #         ).first()
    #         return search
    #     except Exception as e:
    #         self.log.errorExc(None,e,traceback)
    #         return None
