from ..logic.ModelManager import *
from ...model.notification import *
from sqlalchemy import desc


class AlertManager (ModelManager):

    def __init__(self):
        super().__init__(Alert)

    def findAlertsByUser(self,user_id):
        try:
            search = Alert.query.filter(Alert.user_id == user_id).order_by(desc(Alert.created_at)).all()
            return search
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None

    


        