from ...model.profile import *
from ...utilities.responses import *
from ...utilities.loger import *
from .ServiceManager import *



response_util = WebResponse()


class ServiceValidation:
     
    @staticmethod 
    def validateService(name,code):
        isValid = False
        service = ServiceManager().findServiceByCodeAndName(name,code)
        if service is None:
            isValid = True
            response = "Success"   
        elif service.name == name:
            response = "Nombre de servicio ya existe!"
        elif service.code == code:
            response = "Codigo de servicio ya existe!"
        return ValidationResponse(isValid,response)
    

    @staticmethod
    def validateServiceData(service: Service):
        response = any
        isValid = False
        if service.name is None :
            response = "Nombre invalido!"
            return ValidationResponse(isValid,response)
       
        isValid = True
        response = "Success!"
        return ValidationResponse(isValid,response)

    @staticmethod 
    def validateDeleteService(id_service):
       
        isValid = True
        response = "Success!"
        
        return ValidationResponse(isValid,response)