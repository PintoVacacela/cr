from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity

from ...utilities.responses import *
from ...utilities.loger import *

from ...schemas.model_schema import *
from .AssignmentManager import * 


client_schema = ClientSchema()
product_ass_schema = ProductAssignmentSchema()


class AssignmentsView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager= AssigmentManager()


    @jwt_required()
    def get(self):
        clients = self.manager.findClientsAssignments()
        return [client_schema.dump(item) for item in clients],200


    @jwt_required()
    def post(self):
        acces_id = get_jwt_identity()
        client_id = FormatValidator.getStrData(request.form.get("client_id"))
        products = FormatValidator.getStrData(request.form.get("products"))

        if not client_id:
            return response_util.performResponse(400,"No se seleccionó ningun cliente!")
        if not products:
            return response_util.performResponse(400,"No existe ninguna asignacion!")
            
        if products:
            data = FormatValidator.getObjectFromRquestJson(products)
            self.manager.appendProducts(client_id,data)
        
        
       
        self.log.info(acces_id,"Se han realizado las asignaciones exitosamente!")
        return response_util.performResponse(201,"Se han realizado las asignaciones exitosamente!")
    
class ProductAssignmentsView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager= AssigmentManager()


    @jwt_required()
    def get(self, id_client):
        assignments = self.manager.findProductAssingments(id_client)
        return [product_ass_schema.dump(item) for item in assignments],200
    
    @jwt_required()
    def delete(self, id_client):
        acces_id = get_jwt_identity()
        self.manager.deleteAssignments(id_client)
        response = response_util.performResponse(201,"Asignaciones eliminadas exitosamente!")
        self.log.info(acces_id,response)
        return response
    




    