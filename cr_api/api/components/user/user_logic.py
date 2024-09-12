from flask import request
from flask_restful import Resource
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from ...model.user import *
from ...utilities.responses import *
from ...utilities.loger import *
from .user_validation import *
from ..logic.ModelManager import *

user_schema = UserSchema()
validator = UserCreateValidation()

def ValidteEmailFormat(email: str) -> tuple:
    if email is not None:
        try:
            valid = validate_email(email)
            email = valid.email
            return True, email
        except EmailNotValidError as e:
            return False, str(e)
   

class Login(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = UserManager()

    def post(self):
        response = any
        username = request.json["username"]  
        password = request.json["password"]
        user = self.manager.findUserByUserName(username)
        if user is not None:
            if password==user.password:
                access_token = create_access_token(identity = user.id)
                response = response_util.performTokenResponse(200,"Ingreso exitoso!",access_token)
                self.log.info(user.id,response)
                return response
        response = response_util.performResponse(401,"El usuario o la contraseña son incorrectos!")
        self.log.errorExc(None,None,response)
        return response
    

class Users(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = UserManager()

    @jwt_required()
    def get(self):
        users = self.manager.findAll()
        return [user_schema.dump(user) for user in users],200
    
    @jwt_required()
    def post(self):
        acces_id = get_jwt_identity()
        name = request.json["name"]  
        lastname = request.json["lastname"]  
        username = request.json["username"]  
        email = request.json["email"] 
        documentType_id = request.json['documentype']
        identification = request.json["identification"]  
        password = request.json["password"]  
        userType_id = request.json["userType_id"]  
        new_user = ApplicationUser(
            name=name,
            lastname=lastname,
            username=username,
            email=email,
            documentType_id=documentType_id,
            identification=identification,
            password=password,
            userType_id=userType_id
        )
        response = any
        validation = validator.validateUserData(new_user)
        if validation.isValid:
            validation = validator.validateExistenceUser(username,email,identification)
            if validation.isValid:
                self.manager.create(new_user)
                self.log.info(acces_id,validation.response)
                return response_util.performResponse(201,"Usuario creado exitosamente!")
            else:
                response = response_util.performResponse(400,validation.response)
        else:
            response = response_util.performResponse(400,validation.response)
        self.log.errorExc(acces_id,None,validation.response)
        return response
    


class User(Resource):
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
        response = response_util.performResponse(201,"Usuario creado exitosamente!")
        self.log.info(acces_id,response)
        return response
    
    @jwt_required()
    def put(self, id_user):
        acces_id = get_jwt_identity()
        user = self.manager.filterById(id_user)
        if user is None:
            return response_util.performResponse(404,"No se puede encontrar el usuario!")

        name = request.json["name"]  
        lastname = request.json["lastname"]  
        username = request.json["username"]  
        documentType_id = request.json['documentype']
        identification = request.json["identification"]  
        password = request.json["password"]  
        userType_id = request.json["userType_id"]  

        user.name = name if name is not None else user.name
        user.lastname = lastname if lastname is not None else user.lastname
        user.username = username if username is not None else user.username
        user.documentType_id = documentType_id if documentType_id is not None else user.documentType_id
        user.identification = identification if identification is not None else user.identification
        user.password = password if password is not None else user.password
        user.userType_id = userType_id if userType_id is not None else user.userType_id

        validation = validator.validateUserData(user)
        if validation.isValid:
            self.manager.put()
            self.log.info(acces_id,validation.response)
            return response_util.performResponse(201,validation.response)
        else:
            self.log.errorExc(acces_id,None,validation.response)
        return validation.response


        