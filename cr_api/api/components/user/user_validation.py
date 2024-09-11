from ...model.user import *
from ...utilities.responses import *
from ...utilities.loger import *


response_util = WebResponse()

class UserCreateValidation:
     def validateUserData(user: ApplicationUser):
        response = any
        isValid = False
        if user.name is None :
            response = response_util.performResponse(400,"Nombre invalido!")
            return {"isValid":isValid, "response":response}
        if user.lastname is None:
            response = response_util.performResponse(400,"Apellido invalido!")
            return {"isValid":isValid, "response":response}
        if user.username is None  :
            response = response_util.performResponse(400,"Nombre de usuario invalido!")
            return {"isValid":isValid, "response":response}
        if user.documentType_id is None:
            response = response_util.performResponse(400,"Tipo de documento de usuario invalido!")
            return {"isValid":isValid, "response":response}
        if user.identification is None  :
            response = response_util.performResponse(400,"Identificacion de usuario invalido!")
            return {"isValid":isValid, "response":response}
        if user.password is None  :
            response = response_util.performResponse(400,"Contraseña de usuario invalido!")
            return {"isValid":isValid, "response":response}
        if user.userType_id is None  :
            response = response_util.performResponse(400,"Tipo de usuario invalido!")
            return {"isValid":isValid, "response":response}
        isValid = True
        response = response_util.performResponse(201,"Usuario creado exitosamente!")
        return {"isValid":isValid, "response":response}