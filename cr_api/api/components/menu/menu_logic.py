from flask import request
from flask_restful import Resource
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from ...model.menu import *
from ..logic.ModelManager import *
from ...schemas.model_schema import * 
from ..user.UserManager import *
import json


menu_schema = MenuSchema()

def buildMenu(menus):
    if menus is not None:
        menus = list(menus)
        
        parent_menus = [item for item in menus if item["code_parent"] is None]
     
        ordered_menus = []
        for parent_menu in parent_menus:
            children_menus = [item for item in menus if item["code_parent"] == parent_menu["code"]]
            if not children_menus:
                children_menus = []
            else:
                children_menus = sorted(children_menus, key=lambda x: x['position']) 
            parent_menu["submenus"] = children_menus
            ordered_menus.append(parent_menu)
        ordered_menus = sorted(ordered_menus, key=lambda x: x['position'])  
        return ordered_menus



class UserMenusView(Resource):
    def __init__(self):
        self.manager = UserManager()
        self.log = LoggerFactory().get_logger(self.__class__)

    @jwt_required()
    def get(self):
        acces_id = get_jwt_identity()
        user = self.manager.findById(acces_id)
        if user and user.profile:
            menus = user.profile.menus
            response = [menu_schema.dump(menu) for menu in menus]
            return buildMenu(response),200
        
        return response_util.performResponse(404,"No se puede encontrar los menus del usuario!")


        
    
class MenusView(Resource):
    def __init__(self):
        self.manager = ModelManager(ApplicationMenu)

    @jwt_required()
    def get(self):
        menus = self.manager.findActives()
        response = [menu_schema.dump(menu) for menu in menus]
        return buildMenu(response),200
    
   
