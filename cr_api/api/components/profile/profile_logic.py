from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...model.profile import *
from ...utilities.responses import *
from ...utilities.loger import *
from .ProfileManager import *
from ..logic.BaseLogicClass import *
from .profile_validation import * 
from ...schemas.profile_schema import *

profile_schema = ProfileSchema()
validator = ProfileCreateValidation()

class ProfilesView(BaseLogicClass):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ProfileManager()

    @jwt_required()
    def get(self):
        profiles = self.manager.findActives()
        return [profile_schema.dump(item) for item in profiles],200
    
    @jwt_required()
    def post(self):
        acces_id = get_jwt_identity()

        name = request.form.get("name")  
        code = request.form.get("code")  
        menus = request.form.get("menus")  
        new_profile = Profile(
            name = name,
            code = code
        )

        response = any
        validation = validator.validateProfileData(new_profile,menus)
        if validation.isValid:
            validation = validator.validateProfile(name,code)
            if validation.isValid:
                self.manager.create(new_profile)
                self.manager.appendMenus(new_profile,menus)
                self.log.info(acces_id,validation.response)
                return response_util.performResponseObject(201,"Perfil creado exitosamente!",profile_schema.dump(new_profile))
            else:
                response = response_util.performResponse(400,validation.response)
        else:
            response = response_util.performResponse(400,validation.response)
        self.log.error(acces_id,validation.response)
        return response
    


class ProfileView(Resource):
    def __init__(self): 
        self.manager = ProfileManager()
        self.log = LoggerFactory().get_logger(self.__class__)

    @jwt_required()
    def get(self, id_profile):
        return profile_schema.dump(self.manager.findById(id_profile))
    
    @jwt_required()
    def delete(self, id_profile):
        acces_id = get_jwt_identity()
        profile = self.manager.findById(id_profile)
        if profile is None:
            return response_util.performResponse(404,"No se puede encontrar el perfil!")
        response = response_util.performResponse(201,"Perfil eliminado exitosamente!")
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
        menus = request.form.get("menus") 

        profile.name = name if name is not None else profile.name
        profile.code = code if code is not None else profile.code
        validation = validator.validateProfileData(profile)
        if validation.isValid:
            self.manager.put()
            if menus is not None:
                self.manager.appendMenus(profile,menus)
            self.log.info(acces_id,validation.response)
            return  response_util.performResponseObject(200,"Perfil actualizado exitosamente!", profile_schema.dump(profile))
        else:
            self.log.error(acces_id,validation.response)
        return validation.response
    



        