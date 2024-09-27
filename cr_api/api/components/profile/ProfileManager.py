from ..logic.ModelManager import *
from ...model.profile import *
from sqlalchemy import or_

class ProfileManager (ModelManager):

    def __init__(self):
        super().__init__(Profile)

    def appendMenus(self,profile:Profile,menus):
        try:
            ProfileMenus.query.filter_by( ProfileMenus.profile_id==profile.id).delete()
            db.session.commit()
            for item in menus:
                new_item = ProfileMenus(
                    profile_id = profile.id,
                    menu_id = item
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



