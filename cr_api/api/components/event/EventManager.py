from ..logic.ModelManager import *
from ...model.client_service import *
from ..notification.notification_logic import *
from datetime import date
from sqlalchemy import or_

class EventManager (ModelManager):

    def __init__(self):
        super().__init__(Event)

 
    def appendUsers(self,event:Event,users):
        try:
            not_util = NotificationUtils()
            EventUser.query.filter(EventUser.event_id==event.id).delete()
            db.session.commit()
            for item in users:
                new_item = EventUser(
                    event_id = event.id,
                    user_id = int(item)
                )
                db.session.add(new_item)
                db.session.commit()
                message = "Nombre: "+ event.name + "\nFecha:" + event.start_date.strftime("%Y-%m-%d") +"\nCliente:"+event.client.name+"\nDescripcion:"+event.description
                not_util.createInfo(new_item.user_id,message,"Se le ha asignado un evento")
            return event
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        
    def appendServices(self,event:Event,services):
        try:
            EventService.query.filter(EventService.event_id==event.id).delete()
            db.session.commit()
            for item in services:
                new_item = EventService(
                    event_id = event.id,
                    product_id = int(item)
                )
                db.session.add(new_item)
                db.session.commit()
            return event
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        
    def appendDays(self,event:Event,days):
        try:
            EventDay.query.filter(EventDay.event_id==event.id).delete()
            db.session.commit()
            weeckly = False
            if event.frequency_type == frecuency.Semanalmente:
                weeckly = True
            if weeckly:

                for item in days:
                    new_item = EventDay(
                        event_id = event.id,
                        day = item
                    )
                    db.session.add(new_item)
                    db.session.commit()
            else:
                for item in days:
                    new_item = EventDay(
                        event_id = event.id,
                        number_day = int(item)
                    )
                    db.session.add(new_item)
                    db.session.commit()
            return event
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        
    def scheduleEvents(self,event:Event,scheduled):
        try:
            alert_util = AlertUtils()
            event.scheduled.clear()
            db.session.commit()
            for item in scheduled:
                db.session.add(item)
                db.session.commit()
                if item.date == date.today():
                    message = "Nombre: "+ event.name + "\nFecha:" + event.start_date.strftime("%Y-%m-%d")
                    for user in  event.users:
                        alert_util.createWarning(user.id,message,False)
            return event
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        
    