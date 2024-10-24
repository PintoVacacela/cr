from . import db
from .model import *

class event_type(Enum):
    Mantenimiento = 1
    Capacitacion = 2
    Visita = 3
    Evento = 4

class day(Enum):
    Lunes = 0
    Martes = 1
    Miercoles = 2
    Jueves = 3
    Viernes = 4
    Sabado = 5
    Domingo = 6

class frecuency(Enum):
    Semanalmente = 1
    Mensualmente = 2
    
class Service(BasicModel):
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(600))
    price = db.Column(db.Float) 
    code = db.Column(db.String(200))
    events = db.relationship('Event', secondary='event_service', back_populates='services')

class Event(BasicModel):
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(600))
    type = db.Column(db.Enum(event_type), default='Evento')
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    frequency_type = db.Column(db.Enum(frecuency), nullable=False)   # Ej. "weekly", "daily", "monthly"
    frequency_value = db.Column(db.Integer, nullable=False)  # Ej. 1 para "una vez", 2 para "dos veces"
    days = db.relationship("EventDay", back_populates="event", cascade="all, delete-orphan")
    has_price = db.Column(db.Boolean)
    price = db.Column(db.Float) 
    address = db.Column(db.String(600))
    is_obligatory = db.Column(db.Boolean)
    users = db.relationship('ApplicationUser', secondary='event_user', back_populates='events')
    services = db.relationship('Service', secondary='event_service', back_populates='events')
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    client = db.relationship("Client", back_populates="events")
    scheduled = db.relationship('ScheduledEvent', cascade="all, delete-orphan")

class ScheduledEvent(BasicModel):
    date = db.Column(db.Date, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    event = db.relationship("Event", back_populates="scheduled")

class EventDay(BasicModel):
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship("Event", back_populates="days")
    day = db.Column(db.Enum(day))
    number_day = db.Column(db.Integer)

class EventUser(db.Model):
    event_id = db.Column(db.Integer, db.ForeignKey('event.id') ,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('application_user.id') ,primary_key=True)


class EventService(db.Model):
    event_id = db.Column(db.Integer, db.ForeignKey('event.id') ,primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id') ,primary_key=True)

class ServiceClient(db.Model):
    service_id = db.Column(db.Integer, db.ForeignKey('service.id') ,primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id') ,primary_key=True)
    price = db.Column(db.Float) 
    is_programed = db.Column(db.Boolean)
