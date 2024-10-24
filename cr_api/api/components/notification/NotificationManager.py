from ..logic.ModelManager import *
from ...model.notification import *
from sqlalchemy import desc


class NotificationManager (ModelManager):

    def __init__(self):
        super().__init__(UserNotification)

    def findNotificationsByUser(self,user_id):
        try:
            search = UserNotification.query.filter(UserNotification.user_id == user_id).order_by(desc(UserNotification.created_at)).limit(10).all()
            return search
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        
    def findAllNotificationsByUser(self,user_id):
        try:
            search = UserNotification.query.filter(UserNotification.user_id == user_id).order_by(desc(UserNotification.created_at)).all()
            return search
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None


        