from ...model.client_service import *
from ...components.notification.notification_logic import *
from datetime import date

def create_diary_alerts():

    print("Esta tarea se ejecuta al inicio del día.")

def events_alerts():
    today_events = ScheduledEvent.query.filter(ScheduledEvent.date == date.today()).all()
    for event in today_events:
        message = "Nombre: "+ event.name + "\nFecha:" + event.start_date
        for user in event.event.users:
            AlertUtils.createDanger(user.id,message,False)
            
