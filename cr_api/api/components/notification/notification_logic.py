from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity

from ...utilities.responses import *
from ...utilities.loger import *

from ...schemas.model_schema import *

from .NotificationManager import *
from .AlertManager import *

from ...utilities.socket.socket_events import *


notification_schema = UserNotificationSchema()
alert_schema = AlertSchema()

class NotificationUtils:

    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = NotificationManager()


    def createInfo(self,user_id,message,title):
        notification = UserNotification(
            type='INFO',
            title=title,
            message=message,
            opened=False,
            user_id=user_id
        )
        self.manager.create(notification)
        emit_notification_to_user(user_id,notification_schema.dump(notification))


    def createWarning(self,user_id,message,title):
        notification = UserNotification(
            type='WARNING',
            title=title,
            message=message,
            opened=False,
            user_id=user_id
        )
        self.manager.create(notification)
        emit_notification_to_user(user_id,notification_schema.dump(notification))

    def createDanger(self,user_id,message,title ):
        notification = UserNotification(
            type='DANGER',
            title =title ,
            message=message,
            opened=False,
            user_id=user_id
        )
        self.manager.create(notification)
        emit_notification_to_user(user_id,notification_schema.dump(notification))

class AlertUtils:

    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = AlertManager()


    def createInfo(self,user_id,message,is_general):
        alert = Alert(
            type='INFO',
            message=message,
            is_general=is_general,
            user_id=user_id
        )
        self.manager.create(alert)
        emit_alert_to_user(user_id,alert_schema.dump(alert))


    def createWarning(self,user_id,message,is_general):
        alert = Alert(
            type='WARNING',
            message=message,
            is_general=is_general,
            user_id=user_id
        )
        self.manager.create(alert)
        emit_alert_to_user(user_id,alert_schema.dump(alert))
        

    def createDanger(self,user_id,message,is_general):
        alert = Alert(
            type='DANGER',
            message=message,
            is_general=is_general,
            user_id=user_id
        )
        self.manager.create(alert)
        emit_alert_to_user(user_id,alert_schema.dump(alert))
        


class NotificationsView(Resource):
    def __init__(self): 
        self.manager = NotificationManager()
        self.log = LoggerFactory().get_logger(self.__class__)

    @jwt_required()
    def get(self):
        acces_id = get_jwt_identity()
        notifications = self.manager.findNotificationsByUser(acces_id)
        return [notification_schema.dump(item) for item in notifications],200



class NotificationsAllView(Resource):
    def __init__(self): 
        self.manager = NotificationManager()
        self.log = LoggerFactory().get_logger(self.__class__)

    @jwt_required()
    def get(self):
        acces_id = get_jwt_identity()
        notifications = self.manager.findAllNotificationsByUser(acces_id)
        return [notification_schema.dump(item) for item in notifications],200

class NotificationView(Resource):
    def __init__(self): 
        self.manager = NotificationManager()
        self.log = LoggerFactory().get_logger(self.__class__)

    @jwt_required()
    def put(self, id_notification):
        notification = self.manager.findById(id_notification)
        if notification is None:
            return response_util.performResponse(404,"No se puede encontrar la notificacion!")
        notification.opened = True
        self.manager.put()
        return response_util.performResponse(200,"Notificacion leida!")
    

class AlertsView(Resource):
    def __init__(self): 
        self.manager = AlertManager()
        self.log = LoggerFactory().get_logger(self.__class__)

    @jwt_required()
    def get(self):
        acces_id = get_jwt_identity()
        alerts = self.manager.findAlertsByUser(acces_id)
        return [alert_schema.dump(item) for item in alerts],200


        