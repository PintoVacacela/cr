from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...model.profile import *
from ...utilities.responses import *
from ...utilities.loger import *
from .ClientCateoryManager import *
from ..logic.BaseLogicClass import *
from .client_validation import * 
from ...schemas.model_schema import *
from ...utilities.customized.FormatValidation import *

category_schema = ClientCategorySchema()
validator = ClientCategoryValidator()

def buildCateoryTree(parents,categorys):
    category_tree = []
    if parents:
        for parent in parents:
            childrens = [item for item in categorys if item["parent_id"] == parent["id"]]
            if childrens :
                childrens = sorted(childrens, key=lambda x: x['name']) 
                childrens = buildCateoryTree(childrens, categorys)
            parent["subcategorys"] = childrens
            category_tree.append(parent)
        return category_tree

class ClientCategorysView(BaseLogicClass):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ClientCategoryManager()

    @jwt_required()
    def get(self):
        categories = self.manager.findAll()
        return [category_schema.dump(item) for item in categories],200
    
    @jwt_required()
    def post(self):
        acces_id = get_jwt_identity()
        code = request.form.get("code") 
        name = request.form.get("name") 
        parent_id = request.form.get("parent_id") 
        new_category = ClientCategory(
            name = name,
            code = code,
            parent_id=parent_id
        )
        response = any
        
        validation = validator.validateCategoryData(new_category)
        if validation.isValid:
            self.manager.create(new_category)
            self.log.info(acces_id,validation.response)
            return response_util.performResponseObject(201,"Categoria creada exitosamente!",category_schema.dump(new_category))
        else:
            response = response_util.performResponse(400,validation.response)
        self.log.error(acces_id,validation.response)
        return response
    
class ClientCategoryTreeView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ClientCategoryManager()

    @jwt_required()
    def get(self):
        categories = self.manager.findActives()
        categories = [category_schema.dump(menu) for menu in categories]
        response = []
        if categories is not None:
            categorys = list(categories)
            parent_categorys = [item for item in categorys if item["parent_id"] == 0]
            response = buildCateoryTree(parent_categorys,categorys)
        return response,200

class ClientCategoryView(Resource):
    def __init__(self): 
        self.manager = ClientCategoryManager()
        self.log = LoggerFactory().get_logger(self.__class__)

    @jwt_required()
    def get(self, id_category):
        return category_schema.dump(self.manager.findById(id_category))
    
    @jwt_required()
    def delete(self, id_category):
        acces_id = get_jwt_identity()
        category = self.manager.findById(id_category)
        validation = validator.validateDeleteCategory(id_category)
        if not validation.isValid:
            return response_util.performResponse(404,validation.response)
        if category is None:
            return response_util.performResponse(404,"No se puede encontrar la categoria!")
        self.manager.delete(category)
        response = response_util.performResponse(201,"Categoria eliminada exitosamente!")
        self.log.info(acces_id,response)
        return response
    
    @jwt_required()
    def put(self, id_profile):
        acces_id = get_jwt_identity()
        profile = self.manager.findById(id_profile)
        if profile is None:
            return response_util.performResponse(404,"No se puede encontrar el perfil!")

        name = request.form.get("name")  
        code = request.form.get("code")  
        
        profile.name = name if not FormatValidator.isNullOrEmpty(name) else type.name
        profile.code = code if not FormatValidator.isNullOrEmpty(code) else type.code
        validation = validator.validateCategoryData(profile)
        if validation.isValid:
            self.manager.put()
            self.log.info(acces_id,validation.response)
            return  response_util.performResponseObject(200,"Perfil actualizado exitosamente!", category_schema.dump(profile))
        else:
            self.log.error(acces_id,validation.response)
        return validation.response