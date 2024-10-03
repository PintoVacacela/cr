from ...model.user import *
from ...model.profile import *
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
            response = "Email de usuario ya existe!"
        elif new_user.username == username:
            response = "Nombre de usuario ya existe!"
        elif new_user.identification == identification:
            response = "Identificacion de usuario ya existe!"
        return ValidationResponse(isValid,response)
    
    @staticmethod 
    def validateExistenceUserUpdate(id,username,email,identification):
        isValid = False
        new_user = UserManager().findRegisteredUserWithoutId(id,username,email,identification)
        if new_user is None:
            isValid = True
            response = "Success"   
        elif new_user.email == email:
            response = "Email de usuario ya existe!"
        elif new_user.username == username:
            response = "Nombre de usuario ya existe!"
        elif new_user.identification == identification:
            response = "Identificacion de usuario ya existe!"
        return ValidationResponse(isValid,response)



    @staticmethod
    def validateUserData(user: ApplicationUser):
        response = any
        isValid = False
        if  FormatValidator.isNullOrEmpty(user.name):
            response = "Nombre invalido!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(user.lastname):
            response = "Apellido invalido!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(user.username) :
            response = "Nombre de usuario invalido!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(user.email) :
            response = "Email de usuario invalido!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(user.documentType_id):
            response = "Tipo de documento de usuario invalido!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(user.identification):
            response = "Identificacion de usuario invalido!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(user.password):
            response = "Contraseña de usuario invalido!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(user.userType_id):
            response = "Tipo de usuario invalido!"
            return ValidationResponse(isValid,response)
        isValid = True
        response = "Success!"
        return ValidationResponse(isValid,response)
    

    @staticmethod
    def validateDocumentData(document: DocumentType):
        response = any
        isValid = False
        if FormatValidator.isNullOrEmpty(document.name):
            response = "Nombre invalido!"
            return ValidationResponse(isValid,response)
        isValid = True
        response = "Success!"
        return ValidationResponse(isValid,response)
    

    @staticmethod
    def validateUserTypeData(type: UserType):
        response = any
        isValid = False
        if FormatValidator.isNullOrEmpty(type.name):
            response = "Nombre invalido!"
            return ValidationResponse(isValid,response)
        isValid = True
        response = "Success!"
        return ValidationResponse(isValid,response)
    
    @staticmethod 
    def validateDeleteDocument(id_document):
        users = ApplicationUser.query.filter(ApplicationUser.documentType_id == id_document).all()
        isValid = True
        response = "Success!"
        if len(users) > 0:
            isValid = False
            response = "No se puede eliminar el tipo de documento, existen usuarios asociados!"
        return ValidationResponse(isValid,response)

    @staticmethod 
    def validateDeleteUserType(id_type):
        users = ApplicationUser.query.filter(ApplicationUser.userType_id == id_type).all()
        isValid = True
        response = "Success!"
        if len(users) > 0:
            isValid = False
            response = "No se puede eliminar el tipo de usuario, existen usuarios asociados!"

        profiles = ProfileUserTypes.query.filter(ProfileUserTypes.user_type_id == id_type).all()
        if len(profiles) > 0:
            isValid = False
            response = "No se puede eliminar el tipo de usuario, existen perfiles asociados!"
        
        return ValidationResponse(isValid,response)