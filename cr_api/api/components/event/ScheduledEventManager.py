from ..logic.ModelManager import *
from ...model.client_service import *
from ...model.user import *
from sqlalchemy import or_

class ScheduledEventManager (ModelManager):

    def __init__(self):
        super().__init__(ScheduledEvent)


    def findActivesUser(self, id_user):
        try:
            user_types = []
            users_id = [id_user]
            user = ApplicationUser.query.filter(ApplicationUser.id == id_user).first()
            if user and user.profile:
                user_types = [user_type.id for user_type in user.profile.userTypes]
                other_users = [user.id for user in ApplicationUser.query.filter(ApplicationUser.userType_id.in_(user_types)).all()]
                users_id.extend(other_users)
            events =  ScheduledEvent.query.join(Event).join(Event.users).filter(ApplicationUser.id.in_(users_id)).all()  # Obtener todos los resultados
            return events
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None

