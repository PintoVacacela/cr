from ...model.profile import *
from ...utilities.responses import *
from ...utilities.loger import *
from .ProfileManager import *



response_util = WebResponse()


class ProfileCreateValidation:
     
    @staticmethod 
    def validateProfile(name,code):
        isValid = False
        new_menu = ProfileManager().findProfileByCodeAndName(name,code)
        if new_menu is None:
            isValid = True
            response = "Success"   
        elif new_menu.name == name:
            response = "Nombre de perfil ya existe!"
        elif new_menu.code == code:
            response = "Codigo de perfil ya existe!"
        return ValidationResponse(isValid,response)
    

    @staticmethod
    def validateProfileData(profile: Profile, menus):
        response = any
        isValid = False
        if profile.name is None :
            response = "Nombre invalido!"
            return ValidationResponse(isValid,response)
        if profile.code is None:
            response = "Codigo invalido!"
            return ValidationResponse(isValid,response)
        if menus is None:
            response = "No hay accesos para el perfil!"
            return ValidationResponse(isValid,response)
        if not menus:
            response = "No hay accesos para el perfil!"
            return ValidationResponse(isValid,response)
        isValid = True
        response = "Success!"
        return ValidationResponse(isValid,response)

    @staticmethod 
    def validateDeleteProfile(id_profile):
        users = ApplicationUser.query.filter(ApplicationUser.profile_id == id_profile).all()
        isValid = True
        response = "Success!"
        if len(users) > 0:
            isValid = False
            response = "No se puede eliminar el perfil, existen usuarios asociados!"
        return ValidationResponse(isValid,response)