from ...model.client import *
from ...utilities.responses import *
from ...utilities.loger import *
from .ClientManager import *



class ClientValidator:

    @staticmethod 
    def validateExistenceUser(cedula):
        isValid = False
        new_user = ClientManager().findRegisteredClient(cedula)
        if new_user is None:
            isValid = True
            response = "Success"   
        elif new_user.cedula == cedula:
            response = "Cédula ya existe!"
        return ValidationResponse(isValid,response)
    
    @staticmethod
    def validateClientData(client: Client):
        response = any
        isValid = False
        if  FormatValidator.isNullOrEmpty(client.name):
            response = "Nombre o Razón Social inválido!"
            return ValidationResponse(isValid,response)
        # if  FormatValidator.isNullOrEmpty(user.es_proveedor):
        #     response = "Es proveedor invalido!"
        #     return ValidationResponse(isValid,response)
        # if FormatValidator.isNullOrEmpty(user.es_cliente) :
        #     response = "Es cliente invalido!"
        #     return ValidationResponse(isValid,response)
        # if FormatValidator.isNullOrEmpty(user.tipo) :
        #     response = "Tipo invalido!"
        #     return ValidationResponse(isValid,response)
        # if FormatValidator.isNullOrEmpty(user.razon_social):
        #     response = "Razon social invalida!"
        #     return ValidationResponse(isValid,response)
        # if FormatValidator.isNullOrEmpty(user.es_cliente):
        #     response = "Es cliente invalido!"
        #     return ValidationResponse(isValid,response)
        isValid = True
        response = "Success!"
        return ValidationResponse(isValid,response)
    
    @staticmethod 
    def validateDeleteClient(client):
        contacts = ContactInfo.query.filter(ContactInfo.client_id == client.id).all()
        isValid = True
        response = "Success!"
        if len(contacts) > 0:
            for contact in  contacts:
                result = ClientValidator.validateDeleteContact(contact)
                if not result.isValid:
                    isValid = False
                    response = "No se puede eliminar el cliente, existen contactos asociados en uso!"

        addresses = DeliveryAddress.query.filter(DeliveryAddress.client_id == client.id).all()
        if len(addresses) > 0:
            for address in  addresses:
                result = ClientValidator.validateDeleteAddress(address)
                if not result.isValid:
                    isValid = False
                    response = "No se puede eliminar el cliente, existen direcciones asociadas en uso!"
        return ValidationResponse(isValid,response)
    
    @staticmethod 
    def validateDeleteContact(contact):
        #TO DO delete contact logic
        isValid = True
        response = "Success!"
        return ValidationResponse(isValid,response)
    
    @staticmethod 
    def validateDeleteAddress(address):
        #TO DO delete address logic
        isValid = True
        response = "Success!"
        return ValidationResponse(isValid,response)

class ClientCategoryValidator:

    @staticmethod
    def validateCategoryData(category: ClientCategory):
        response = any
        isValid = False
        if FormatValidator.isNullOrEmpty(category.name):
            response = "Nombre invalido!"
            return ValidationResponse(isValid,response)
        isValid = True
        response = "Success!"
        return ValidationResponse(isValid,response)
    
    @staticmethod 
    def validateDeleteCategory(id_category):
        users = Client.query.filter(Client.category_id == id_category).all()
        isValid = True
        response = "Success!"
        if len(users) > 0:
            isValid = False
            response = "No se puede eliminar la categoria, existen clientes asociados!"
        return ValidationResponse(isValid,response)
    
