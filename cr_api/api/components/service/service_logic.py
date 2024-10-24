from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...model.client_service import *
from ...utilities.responses import *
from ...utilities.loger import *
from .ServiceManager import *
from ..logic.BaseLogicClass import *
from .service_validation import * 
from ...schemas.model_schema import *
from ...utilities.customized.FormatValidation import *

service_schema = ServiceSchema()
validator = ServiceValidation()

class ServicesView(BaseLogicClass):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ServiceManager()

    @jwt_required()
    def get(self):
        services = self.manager.findActives()
        return [service_schema.dump(item) for item in services],200
    
    @jwt_required()
    def post(self):
        acces_id = get_jwt_identity()
        name = FormatValidator.getStrData(request.form.get("name"))  
        description = FormatValidator.getStrData(request.form.get("description"))
        price = FormatValidator.getStrData(request.form.get("price"))  
        code = FormatValidator.getStrData(request.form.get("code"))
        
        new_service = Service(
            name = name,
            description = description,
            price = price,
            code = code
        )
        response = any
        
        validation = validator.validateServiceData(new_service)
        if validation.isValid:
            validation = validator.validateService(name,code)
            if validation.isValid:
                self.manager.create(new_service)
                self.log.info(acces_id,validation.response)
                return response_util.performResponseObject(201,"Perfil creado exitosamente!",service_schema.dump(new_service))
            else:
                response = response_util.performResponse(400,validation.response)
        else:
            response = response_util.performResponse(400,validation.response)
        self.log.error(acces_id,validation.response)
        return response
    


class ServiceView(Resource):
    def __init__(self): 
        self.manager = ServiceManager()
        self.log = LoggerFactory().get_logger(self.__class__)

    @jwt_required()
    def get(self, id_service):
        return service_schema.dump(self.manager.findById(id_service))
    
    @jwt_required()
    def delete(self, id_service):
        acces_id = get_jwt_identity()
        service = self.manager.findById(id_service)
        validation = validator.validateDeleteService(id_service)
        if not validation.isValid:
            return response_util.performResponse(404,validation.response)
        if service is None:
            return response_util.performResponse(404,"No se puede encontrar el servicio!")
        self.manager.delete(service)
        response = response_util.performResponse(201,"Servicio eliminado exitosamente!")
        self.log.info(acces_id,response)
        return response
    
    @jwt_required()
    def put(self, id_service):
        acces_id = get_jwt_identity()
        service = self.manager.findById(id_service)
        if service is None:
            return response_util.performResponse(404,"No se puede encontrar el servicio!")

        name = FormatValidator.getStrData(request.form.get("name"))  
        description = FormatValidator.getStrData(request.form.get("description"))
        price = FormatValidator.getStrData(request.form.get("price"))
        code = FormatValidator.getStrData(request.form.get("code"))  

        service.name = name 
        service.description = description 
        service.price = price 
        service.code = code 
        validation = validator.validateServiceData(service)
        if validation.isValid:
            self.manager.put()
            self.log.info(acces_id,validation.response)
            return  response_util.performResponseObject(200,"Servicio actualizado exitosamente!", service_schema.dump(service))
        else:
            self.log.error(acces_id,validation.response)
        return validation.response
    



        