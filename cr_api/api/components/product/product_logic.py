from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity

from ...utilities.responses import *
from ...utilities.loger import *

from ...schemas.model_schema import *
from .ProductManager import * 



product_schema = ProductSchema()



class ContificoProductsView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ProductManager()

    @jwt_required()
    def get(self):
        products = self.manager.getProductData()
        if products:
            return True,200
        return response_util.performResponse(404,"No se pudo obtener la lista!")





class ProductsView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ProductManager()

    @jwt_required()
    def get(self):
        products = self.manager.findAll()
        return [product_schema.dump(item) for item in products],200
    
class ServicesView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ProductManager()

    @jwt_required()
    def get(self):
        products = self.manager.findProductsPerType("SER")
        return [product_schema.dump(item) for item in products],200
    
class ClientProductView(Resource):

    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ProductManager()

    @jwt_required()
    def get(self, id_client):
        print(id_client)
        return self.manager.findProductsAndAssignments(id_client)
    