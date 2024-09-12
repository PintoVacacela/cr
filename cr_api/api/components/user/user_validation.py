from ...model.user import *
from ...utilities.responses import *
from ...utilities.loger import *
from .UserManager import *



response_util = WebResponse()


class UserCreateValidation:
     
    @staticmethod 
    def validateExistenceUser(username,email,identification):
        isValid = False
        new_user = UserManager().findRegisteredUser(username,email,identification)
        if new_user is None:
            isValid = True
            response = "Success"   
        elif new_user.email == email:
            response = "Email ya existe!"
        elif new_user.username == username:
            response = "Identificacion ya existe!"
        elif new_user.identification == identification:
            response = "Nombre de usuario ya existe!"
        return ValidationResponse(isValid,response)



    @staticmethod
    def validateUserData(user: ApplicationUser):
        response = any
        isValid = False
        if user.name is None :
            response = "Nombre invalido!"
            return ValidationResponse(isValid,response)
        if user.lastname is None:
            response = "Apellido invalido!"
            return ValidationResponse(isValid,response)
        if user.username is None  :
            response = "Nombre de usuario invalido!"
            return ValidationResponse(isValid,response)
        if user.email is None  :
            response = "Email de usuario invalido!"
            return ValidationResponse(isValid,response)
        if user.documentType_id is None:
            response = "Tipo de documento de usuario invalido!"
            return ValidationResponse(isValid,response)
        if user.identification is None  :
            response = "Identificacion de usuario invalido!"
            return ValidationResponse(isValid,response)
        if user.password is None  :
            response = "Contraseña de usuario invalido!"
            return ValidationResponse(isValid,response)
        if user.userType_id is None  :
            response = "Tipo de usuario invalido!"
            return ValidationResponse(isValid,response)
        isValid = True
        response = "Success!"
        return ValidationResponse(isValid,response)