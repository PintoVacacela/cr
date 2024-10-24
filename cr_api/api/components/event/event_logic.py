from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...model.client_service import *
from ...utilities.responses import *
from ...utilities.loger import *
from .EventManager import *
from .ScheduledEventManager import *
from ..logic.BaseLogicClass import *
from .event_validation import * 
from ...schemas.model_schema import *
from ...utilities.customized.FormatValidation import *
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

event_schema = EventSchema()
scheduled_event_schema = ScheduledEventSchema()
validator = EventValidation()

def create_scheduled_events(event: Event):
    scheduled_events = []
    def add_event(date):
        scheduled_events.append(ScheduledEvent(
            date=date,
            event_id=event.id
        ))

    # Obtener el inicio y fin de la fecha
    current_date = event.start_date
    end_date = event.end_date if event.end_date else None
    # Función para agregar eventos programados
    
    if end_date == current_date:
        add_event(current_date)
        return scheduled_events

        # Agregar evento programado basado en la frecuencia
    if event.frequency_type == frecuency.Semanalmente:
        while current_date < end_date:
            if current_date.weekday() in [day.day.value for day in event.days]:
                add_event(current_date)
            if current_date.weekday() == 6:
                current_date += timedelta(days=(7 * (event.frequency_value-1))+1)
            else:    
                current_date += timedelta(days=1)

    elif event.frequency_type == frecuency.Mensualmente:
        while current_date < end_date:
            current_month = current_date.month
            if current_date.day in [day.number_day for day in event.days]:
                add_event(current_date)
            current_date += timedelta(days=1)
            if current_month != current_date.month:
                current_date = current_date + relativedelta(months=event.frequency_value-1)
                current_date = date(current_date.year, current_date.month, 1)

    # elif event.frequency_type == frecuency.Anualmente:
    #     add_event(current_date)
    #     current_date = current_date + timedelta(days=365 * event.frequency_value)

        # Si el evento es semanal, incrementar por cada día especificado
    # if event.frequency_type == frecuency.Semanalmente:
    #     current_date += timedelta(days=1)
    #     continue

    #     # Asegúrate de no salir del rango de fechas
    # if end_date and current_date > end_date:
    #     break

    return scheduled_events

class ScheduledEventsView(BaseLogicClass):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ScheduledEventManager()

    @jwt_required()
    def get(self):
        acces_id = get_jwt_identity()
        events = self.manager.findActivesUser(acces_id)
        return [scheduled_event_schema.dump(item) for item in events],200

class EventsView(BaseLogicClass):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = EventManager()

    @jwt_required()
    def get(self):
        events = self.manager.findActives()
        return [event_schema.dump(item) for item in events],200
    
    @jwt_required()
    def post(self):
        acces_id = get_jwt_identity()
        name = FormatValidator.getStrData(request.form.get("name"))
        description = FormatValidator.getStrData(request.form.get("description"))
        type = FormatValidator.getStrData(request.form.get("type"))
        start_date = FormatValidator.getStrData(request.form.get("start_date"))
        end_date = FormatValidator.getStrData(request.form.get("end_date"))
        frequency_type = FormatValidator.getStrData(request.form.get("frequency_type"))
        frequency_value = FormatValidator.getStrData(request.form.get("frequency_value"))
        days = FormatValidator.getListFomrString(request.form.get("days"))
        has_price = FormatValidator.getBooleanFromString(request.form.get("has_price"))
        price = FormatValidator.getStrData(request.form.get("price"))
        address = FormatValidator.getStrData(request.form.get("address"))
        is_obligatory = FormatValidator.getBooleanFromString(request.form.get("is_obligatory"))
        client_id = FormatValidator.getStrData(request.form.get("client_id"))
        state = FormatValidator.getStrData(request.form.get("state"))
        users = FormatValidator.getListFomrString(request.form.get("users"))
        services = FormatValidator.getListFomrString(request.form.get("services"))
        new_event = Event(
            name= name,
            description= description,
            type= type,
            start_date= start_date,
            end_date= end_date,
            frequency_type= frequency_type,
            frequency_value= frequency_value,
            has_price = has_price,
            price= price,
            address = address,
            is_obligatory= is_obligatory,
            client_id= client_id,
            state = state
        )
        response = any
        
        if not services:
            return response_util.performResponse(400,"No existe ningun servicio seleccionado!")
        if not days:
            return response_util.performResponse(400,"No existe ningun dia seleccionado!")
        validation = validator.validateEventData(new_event)
        if validation.isValid:
            self.manager.create(new_event)
            self.manager.appendUsers(new_event,users)
            self.manager.appendServices(new_event,services)
            self.manager.appendDays(new_event,days)
            self.manager.scheduleEvents(new_event,create_scheduled_events(new_event))
            self.log.info(acces_id,validation.response)
            return response_util.performResponseObject(201,"Evento creado exitosamente!",event_schema.dump(new_event))
        else:
            response = response_util.performResponse(400,validation.response)
        
        self.log.error(acces_id,validation.response)
        return response
    

    


class EventView(Resource):
    def __init__(self): 
        self.manager = EventManager()
        self.log = LoggerFactory().get_logger(self.__class__)

    @jwt_required()
    def get(self, id_event):
        return event_schema.dump(self.manager.findById(id_event))
    
    @jwt_required()
    def delete(self, id_event):
        acces_id = get_jwt_identity()
        event = self.manager.findById(id_event)
        validation = validator.validateDeleteEvent(id_event)
        if not validation.isValid:
            return response_util.performResponse(404,validation.response)
        if event is None:
            return response_util.performResponse(404,"No se puede encontrar el evento!")
        event.users.clear()
        event.services.clear()
        self.manager.delete(event)
        response = response_util.performResponse(201,"Evento eliminado exitosamente!")
        self.log.info(acces_id,response)
        return response
    
    @jwt_required()
    def put(self, id_event):
        acces_id = get_jwt_identity()
        event = self.manager.findById(id_event)
        if event is None:
            return response_util.performResponse(404,"No se puede encontrar el evento!")

        name = FormatValidator.getStrData(request.form.get("name"))
        description = FormatValidator.getStrData(request.form.get("description"))
        type = FormatValidator.getStrData(request.form.get("type"))
        start_date = FormatValidator.getStrData(request.form.get("start_date"))
        end_date = FormatValidator.getStrData(request.form.get("end_date"))
        frequency_type = FormatValidator.getStrData(request.form.get("frequency_type"))
        frequency_value = FormatValidator.getStrData(request.form.get("frequency_value"))
        days = FormatValidator.getListFomrString(request.form.get("days"))
        has_price = FormatValidator.getBooleanFromString(request.form.get("has_price"))
        price = FormatValidator.getStrData(request.form.get("price"))
        address = FormatValidator.getStrData(request.form.get("address"))
        is_obligatory = FormatValidator.getBooleanFromString(request.form.get("is_obligatory"))
        client_id = FormatValidator.getStrData(request.form.get("client_id"))
        state = FormatValidator.getStrData(request.form.get("state"))

        users = FormatValidator.getListFomrString(request.form.get("users"))
        services = FormatValidator.getListFomrString(request.form.get("services"))

        event.name = name       
        event.description = description 
        event.type = type 
        event.start_date = start_date 
        event.end_date = end_date 
        event.frequency_type = frequency_type 
        event.frequency_value = frequency_value 
        event.has_price = has_price
        event.price = price 
        event.address = address
        event.is_obligatory = is_obligatory 
        event.client_id = client_id 
        event.state = state

        validation = validator.validateEventData(event)
        if not services:
            return response_util.performResponse(400,"No existe ningun servicio seleccionado!")
        if not days:
            return response_util.performResponse(400,"No existe ningun dia seleccionado!")
        if validation.isValid:
            self.manager.put()
            self.manager.appendUsers(event,users)
            self.manager.appendServices(event,services)
            self.manager.appendDays(event,days)
            self.manager.scheduleEvents(event,create_scheduled_events(event))
            self.log.info(acces_id,validation.response)
            return  response_util.performResponseObject(200,"Servicio actualizado exitosamente!", event_schema.dump(event))
        else:
            self.log.error(acces_id,validation.response)
        return response_util.performResponse(400,validation.response)
    



class FrecuencyTypeView(Resource):
    @jwt_required()
    def get(self):
        obj = []
        for k in frecuency:
            obj.append({"key":k.name, "value":k.value})
        return obj
    
class EventTypeView(Resource):
    @jwt_required()
    def get(self):
        obj = []
        for k in event_type:
            obj.append({"key":k.name, "value":k.value})
        return obj