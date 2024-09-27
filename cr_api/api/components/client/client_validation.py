from ...model.client import *
from ...utilities.responses import *
from ...utilities.loger import *
from .ClientManager import *



class ClientValidation:

    @staticmethod 
    def validateExistenceUser(cedula):
        isValid = False
        new_user = ClientManager().findRegisteredClient(cedula)
        if new_user is None:
            isValid = True
            response = "Success"   
        elif new_user.cedula == cedula:
            response = "Cedula ya existe!"
        return ValidationResponse(isValid,response)
    
    @staticmethod
    def validateClientData(user: Client):
        response = any
        isValid = False
        if  FormatValidator.isNullOrEmpty(user.cedula):
            response = "Cedula invalido!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(user.es_proveedor):
            response = "Es proveedor invalido!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(user.es_cliente) :
            response = "Es cliente invalido!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(user.tipo) :
            response = "Tipo invalido!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(user.razon_social):
            response = "Razon social invalida!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(user.es_cliente):
            response = "Es cliente invalido!"
            return ValidationResponse(isValid,response)
        isValid = True
        response = "Success!"
        return ValidationResponse(isValid,response)
    
