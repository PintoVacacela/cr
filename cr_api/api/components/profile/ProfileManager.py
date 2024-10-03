from ..logic.ModelManager import *
from ...model.profile import *
from ...model.user import *
from sqlalchemy import or_

class ProfileManager (ModelManager):

    def __init__(self):
        super().__init__(Profile)

    def appendMenus(self,profile:Profile,menus):
        try:
            ProfileMenus.query.filter(ProfileMenus.profile_id==profile.id).delete()
            db.session.commit()
            for item in menus:
                new_item = ProfileMenus(
                    profile_id = profile.id,
                    menu_id = int(item)
                )
                db.session.add(new_item)
                db.session.commit()
            return new_item
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        
    def appendTypes(self,profile:Profile,userTypes):
        try:
            ProfileUserTypes.query.filter(ProfileUserTypes.profile_id==profile.id).delete()
            db.session.commit()
            for item in userTypes:
                new_item = ProfileUserTypes(
                    profile_id = profile.id,
                    user_type_id = int(item)
                )
                db.session.add(new_item)
                db.session.commit()
            return new_item
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None


    def findProfileByCodeAndName(self,name,code):
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
    
    def delete(self,object):
        try:
            ProfileMenus.query.filter(ProfileMenus.profile_id==object.id).delete()
            ProfileUserTypes.query.filter(ProfileUserTypes.profile_id==object.id).delete()
            db.session.delete(object)
            db.session.commit()
            return True
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return False



