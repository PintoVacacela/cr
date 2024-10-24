from flask import request, jsonify, send_from_directory
from flask_restful import Resource
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from ...model.user import *
from ...utilities.responses import *
from ...utilities.loger import *
from .user_validation import *
from ..logic.ModelManager import *
from ...schemas.model_schema import *
from ...utilities.uploaded_files import * 
from ...utilities.customized.FormatValidation import *
from ..notification.notification_logic import *

user_schema = UserSchema()
document_schema = DocumentTypeSchema()
user_type_schema = UserTypeSchema()
validator = UserCreateValidation()

def ValidteEmailFormat(email: str) -> tuple:
    if email is not None:
        try:
            valid = validate_email(email)
            email = valid.email
            return True, email
        except EmailNotValidError as e:
            return False, str(e)
   

class LoginView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = UserManager()

    @jwt_required()
    def get(self):
        acces_id = get_jwt_identity()
        return user_schema.dump(self.manager.findById(acces_id))

    def post(self):
        response = any
        username = FormatValidator.getStrData(request.form.get("username"))  
        password = FormatValidator.getStrData(request.form.get("password"))
        user = self.manager.findUserByUserName(username)
        if user is not None:
            if password==user.password:
                access_token = create_access_token(identity = user.id)
                response = response_util.performTokenResponse(200,"Ingreso exitoso!",access_token)
                self.log.info(user.id,response)
                return response
        response = response_util.performResponse(401,"El usuario o la contraseña son incorrectos!")
        self.log.error(None,response)
        return response
    
class UsersActiveView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = UserManager()

    @jwt_required()
    def get(self):
        users = self.manager.findActives()
        return [user_schema.dump(item) for item in users],200

class UsersView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = UserManager()

    @jwt_required()
    def get(self):
        users = self.manager.findAll()
        return [user_schema.dump(item) for item in users],200
    
    @jwt_required()
    def post(self):
        acces_id = get_jwt_identity()
        name = FormatValidator.getStrData(request.form.get("name"))
        lastname = FormatValidator.getStrData(request.form.get("lastname"))  
        username = FormatValidator.getStrData(request.form.get("username"))  
        email = FormatValidator.getStrData(request.form.get("email")) 
        designation = FormatValidator.getStrData(request.form.get("designation")) 
        phone_number = FormatValidator.getStrData(request.form.get("phone_number")) 
        documentType_id = FormatValidator.getStrData(request.form.get('documentType_id'))
        identification = FormatValidator.getStrData(request.form.get("identification"))  
        password = FormatValidator.getStrData(request.form.get("password"))  
        userType_id = FormatValidator.getStrData(request.form.get("userType_id")) 
        profile_id = FormatValidator.getStrData(request.form.get("profile_id")) 
        state = FormatValidator.getStrData(request.form.get("state"))
        photo_url = None
        
        new_user = ApplicationUser(
            name=name,
            lastname=lastname,
            username=username,
            email=email,
            designation=designation,
            phone_number=phone_number,
            documentType_id=documentType_id,
            identification=identification,
            password=password,
            userType_id=userType_id,
            photo_url=photo_url,
            profile_id=profile_id,
            state=state
        )
        response = any
        validation = validator.validateUserData(new_user)
        if validation.isValid:
            validation = validator.validateExistenceUser(username,email,identification)
            if validation.isValid:
                self.manager.create(new_user)
                if 'photo' in request.files:
                    photo = request.files['photo']
                    photo_url = UploadUtils.savePhoto(photo,'user')
                    new_user.photo_url = photo_url
                    self.manager.put()
                self.log.info(acces_id,validation.response)
                return response_util.performResponseObject(201,"Usuario creado exitosamente!",user_schema.dump(new_user))
            else:
                response = response_util.performResponse(400,validation.response)
        else:
            response = response_util.performResponse(400,validation.response)
        self.log.error(acces_id,validation.response)
        return response
    


class UserView(Resource):
    def __init__(self):
        self.manager = UserManager()
        self.log = LoggerFactory().get_logger(self.__class__)

    @jwt_required()
    def get(self, id_user):
        return user_schema.dump(self.manager.findById(id_user))
    
    @jwt_required()
    def delete(self, id_user):
        acces_id = get_jwt_identity()
        user = self.manager.findById(id_user)
        if user is None:
            return response_util.performResponse(404,"No se puede encontrar el usuario!")
        if user.photo_url is not None:
            UploadUtils.delete_image(user.photo_url)
        self.manager.delete(user)
        response = response_util.performResponse(201,"Usuario eliminado exitosamente!")
        self.log.info(acces_id,response)
        return response

    
    @jwt_required()
    def put(self, id_user):
        acces_id = get_jwt_identity()
        user = self.manager.findById(id_user)
        if user is None:
            return response_util.performResponse(404,"No se puede encontrar el usuario!")

        name = FormatValidator.getStrData(request.form.get("name"))  
        lastname = FormatValidator.getStrData(request.form.get("lastname"))  
        username = FormatValidator.getStrData(request.form.get("username"))  
        email = FormatValidator.getStrData(request.form.get("email")) 
        designation = FormatValidator.getStrData(request.form.get("designation")) 
        phone_number = FormatValidator.getStrData(request.form.get("phone_number")) 
        documentType_id = FormatValidator.getStrData(request.form.get('documentType_id'))
        identification = FormatValidator.getStrData(request.form.get("identification"))  
        password = FormatValidator.getStrData(request.form.get("password"))  
        userType_id = FormatValidator.getStrData(request.form.get("userType_id"))  
        profile_id = FormatValidator.getStrData(request.form.get("profile_id")) 
        state = FormatValidator.getStrData(request.form.get("state"))

        user.name = name if not FormatValidator.isNullOrEmpty(name) else user.name
        user.lastname = lastname if not FormatValidator.isNullOrEmpty(lastname) else user.lastname
        user.username = username if not FormatValidator.isNullOrEmpty(username) else user.username
        user.email = email if not FormatValidator.isNullOrEmpty(email) else user.email
        user.designation = designation if not FormatValidator.isNullOrEmpty(designation) else user.designation
        user.phone_number = phone_number if not FormatValidator.isNullOrEmpty(phone_number) else user.phone_number
        user.documentType_id = documentType_id if not FormatValidator.isNullOrEmpty(documentType_id) else user.documentType_id
        user.identification = identification if not FormatValidator.isNullOrEmpty(identification) else user.identification
        user.password = password if not FormatValidator.isNullOrEmpty(password) else user.password
        user.userType_id = userType_id if not FormatValidator.isNullOrEmpty(userType_id) else user.userType_id
        user.profile_id = profile_id if not FormatValidator.isNullOrEmpty(profile_id) else user.profile_id
        user.state = state if not FormatValidator.isNullOrEmpty(state) else user.state

        photo_url = None
        
        validation = validator.validateUserData(user)
        if validation.isValid:
            validation = validator.validateExistenceUserUpdate(id_user,username,email,identification)
            if validation.isValid:
                if 'photo' in request.files:
                    photo = request.files['photo']
                    photo_url = UploadUtils.savePhoto(photo,'user')
                    if user.photo_url is not None:
                        UploadUtils.delete_image(user.photo_url)
                    user.photo_url = photo_url

                self.manager.put()
                self.log.info(acces_id,validation.response)
                return response_util.performResponseObject(200,"Usuario actualizado exitosamente!",user_schema.dump(user))
        else:
            self.log.error(acces_id,validation.response)
        return validation.response


class DocumentTypesView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ModelManager(DocumentType)

    @jwt_required()
    def get(self):
        documents = self.manager.findAll()
        return [document_schema.dump(item) for item in documents],200
    
    @jwt_required()
    def post(self):
        acces_id = get_jwt_identity()
        name = FormatValidator.getStrData(request.form.get("name"))  
        state = FormatValidator.getStrData(request.form.get("state"))
        new_document = DocumentType(
            name=name,
            state=state
        )
        response = any
        validation = validator.validateDocumentData(new_document)
        if validation.isValid:
            self.manager.create(new_document)
            self.log.info(acces_id,validation.response)
            return response_util.performResponseObject(201,"Tipo de Documento creado exitosamente!", document_schema.dump(new_document))
            
        else:
            response = response_util.performResponse(400,validation.response)
        self.log.error(acces_id,validation.response)
        return response
    

class DocumentTypeView(Resource):
    def __init__(self):
        self.manager = ModelManager(DocumentType)
        self.log = LoggerFactory().get_logger(self.__class__)

    @jwt_required()
    def get(self, id_document):
        return document_schema.dump(self.manager.findById(id_document))
    
    @jwt_required()
    def delete(self, id_document):
        acces_id = get_jwt_identity()
        document = self.manager.findById(id_document)
        validation = validator.validateDeleteDocument(id_document)
        if not validation.isValid:
            return response_util.performResponse(404,validation.response)
        if document is None:
            return response_util.performResponse(404,"No se puede encontrar el tipo de documento!")
        self.manager.delete(document)
        response = response_util.performResponse(201,"Tipo de documento eliminado exitosamente!")
        self.log.info(acces_id,response)
        return response
    
    @jwt_required()
    def put(self, id_document):
        acces_id = get_jwt_identity()
        document = self.manager.findById(id_document)
        if document is None:
            return response_util.performResponse(404,"No se puede tipo de documento!")

        name = FormatValidator.getStrData(request.form.get("name"))  
        state = FormatValidator.getStrData(request.form.get("state"))
        document.name = name if not FormatValidator.isNullOrEmpty(name) else document.name
        document.state = state if not FormatValidator.isNullOrEmpty(state) else document.state
        validation = validator.validateDocumentData(document)
        if validation.isValid:
            self.manager.put()
            self.log.info(acces_id,validation.response)
            return response_util.performResponseObject(200,"Tipo de Documento actualizado exitosamente!",document_schema.dump(document))
        else:
            self.log.error(acces_id,validation.response)
        return response_util.performResponse(400,validation.response)
    

class UserTypesView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ModelManager(UserType)

    @jwt_required()
    def get(self):
        types = self.manager.findAll()
        return [user_type_schema.dump(item) for item in types],200
    
    @jwt_required()
    def post(self):
        acces_id = get_jwt_identity()
        name = FormatValidator.getStrData(request.form.get("name"))  
        state = FormatValidator.getStrData(request.form.get("state"))
        new_type = UserType(
            name=name,
            state=state
        )
        response = any
        validation = validator.validateDocumentData(new_type)
        if validation.isValid:
            self.manager.create(new_type)
            self.log.info(acces_id,validation.response)
            return response_util.performResponseObject(201,"Tipo de usuario creado exitosamente!", user_type_schema.dump(new_type))
            
        else:
            response = response_util.performResponse(400,validation.response)
        self.log.error(acces_id,validation.response)
        return response
    

class UserTypeView(Resource):
    def __init__(self):
        self.manager = ModelManager(UserType)
        self.log = LoggerFactory().get_logger(self.__class__)

    @jwt_required()
    def get(self, id_type):
        return user_type_schema.dump(self.manager.findById(id_type))
    
    @jwt_required()
    def delete(self, id_type):
        acces_id = get_jwt_identity()
        type = self.manager.findById(id_type)
        validation = validator.validateDeleteUserType(id_type)
        if not validation.isValid:
            return response_util.performResponse(404,validation.response)
        if type is None:
            return response_util.performResponse(404,"No se puede encontrar el tipo de usuario!")
        self.manager.delete(type)
        response = response_util.performResponse(201,"Tipo de usuario eliminado exitosamente!")
        self.log.info(acces_id,response)
        return response
    
    @jwt_required()
    def put(self, id_type):
        acces_id = get_jwt_identity()
        type = self.manager.findById(id_type)
        if type is None:
            return response_util.performResponse(404,"No se puede tipo de usuario!")

        name = FormatValidator.getStrData(request.form.get("name"))  
        state = FormatValidator.getStrData(request.form.get("state"))
        type.name = name if not FormatValidator.isNullOrEmpty(name) else type.name
        type.state = state if not FormatValidator.isNullOrEmpty(state) else type.state

        validation = validator.validateUserTypeData(type)
        if validation.isValid:
            self.manager.put()
            self.log.info(acces_id,validation.response)
            return response_util.performResponseObject(200,"Tipo de usuario actualizado exitosamente!", user_type_schema.dump(type))
        else:
            self.log.error(acces_id,validation.response)
        return response_util.performResponse(400,validation.response)
    


class UserConfigView(Resource):
    def __init__(self):
        self.manager = UserManager()
        self.log = LoggerFactory().get_logger(self.__class__)
    
    @jwt_required()
    def put(self):
        acces_id = get_jwt_identity()
        user = self.manager.findById(acces_id)
        if user is None:
            return response_util.performResponse(404,"No se puede encontrar el usuario!")
        
        passwordActual = FormatValidator.getStrData(request.form.get("passwordActual"))  
        passwordNew = FormatValidator.getStrData(request.form.get("passwordNew"))
        passwordConfirmation = FormatValidator.getStrData(request.form.get("passwordConfirmation"))
        response = None
        if FormatValidator.isNullOrEmpty(passwordActual):
            response = response_util.performResponse(400,"No se ingreso la contraseña actual!")
            return response

        if FormatValidator.isNullOrEmpty(passwordNew):
            response = response_util.performResponse(400,"No se ingreso la contraseña nueva!")
            return response

        if FormatValidator.isNullOrEmpty(passwordConfirmation):
            response = response_util.performResponse(400,"No se confirmó la contraseña nueva!")
            return response
        
        if user.password != passwordActual:
            response = response_util.performResponse(400,"No se ingreso la contraseña actual!")
            return response

        if user.password == passwordNew:
            response = response_util.performResponse(400,"La contraseña debe ser distinta!")
            return response

        if passwordNew != passwordConfirmation:
            response = response_util.performResponse(400,"Las contraseñas nuevas deben coincidir!")
            return response
        
        user.password = passwordNew
        photo_url = None
        
        if 'photo' in request.files:
            photo = request.files['photo']
            photo_url = UploadUtils.savePhoto(photo,'user')
            if user.photo_url is not None:
                UploadUtils.delete_image(user.photo_url)
            user.photo_url = photo_url
        response = response_util.performResponse(200,"Usuario actualizado exitosamente!")
        self.manager.put()
        self.log.info(acces_id,response)
        return response
        
    