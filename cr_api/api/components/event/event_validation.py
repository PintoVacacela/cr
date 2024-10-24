from ...model.profile import *
from ...utilities.responses import *
from ...utilities.loger import *
from .EventManager import *
from ...utilities.customized.FormatValidation import *


response_util = WebResponse()


class EventValidation:
    

    @staticmethod
    def validateEventData(event: Event):
        response = any
        isValid = False
        if event.name is None :
            response = "Nombre invalido!"
            return ValidationResponse(isValid,response)
        if event.type is None:
            response = "Tipo invalido!"
            return ValidationResponse(isValid,response)
        if event.start_date is None:
            response = "Fecha Inicio invalida!"
            return ValidationResponse(isValid,response)
        if event.end_date is None:
            response = "Fecha Fin invalida!"
            return ValidationResponse(isValid,response)
        if event.frequency_type is None:
            response = "Tipo de frecuencia invalida!"
            return ValidationResponse(isValid,response)
        if event.frequency_value is None:
            response = "Frecuencia invalida!"
            return ValidationResponse(isValid,response)
        if not FormatValidator.validateDateFormat(event.start_date):
            response = "Formato Fecha Inicio invalido!"
            return ValidationResponse(isValid,response)
        if not FormatValidator.validateDateFormat(event.end_date):
            response = "Formato Fecha Fin invalido!"
            return ValidationResponse(isValid,response)
        isValid = True
        response = "Success!"
        return ValidationResponse(isValid,response)

    @staticmethod 
    def validateDeleteEvent(id_event):
       
        isValid = True
        response = "Success!"
        
        return ValidationResponse(isValid,response)