from flask import request
from flask_restful import Resource
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from statistics import mean
from ...model.user import *
from ...utilities.responses import *
from ...utilities.loger import *
from .user_validation import *

user_schema = UserSchema()
response_util = WebResponse()
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

    def post(self):
        response = any
        username = request.json["username"]  
        password = request.json["password"]
        user = ApplicationUser.query.filter(ApplicationUser.username==username).first()
        if user is not None:
            if password==user.password:
                access_token = create_access_token(identity = user.id)
                response = response_util.performResponse(200,"Ingreso exitoso!",access_token)
                self.log.info(user.id,response)
                return response
        response = response_util.performResponse(401,"El usuario o la contraseña son incorrectos!")
        self.log.info(response)
        return response
    

class Users(Resource):
    @jwt_required()
    def get(self):
        users = ApplicationUser.query.all()
        return [user_schema.dump(user) for user in users],200
    
    def post(self):
        name = request.json["name"]  
        lastname = request.json["lastname"]  
        username = request.json["username"]  
        documentType_id = request.json['documentype']
        identification = request.json["identification"]  
        password = request.json["password"]  
        userType_id = request.json["userType_id"]  
        new_user = ApplicationUser(
            name=name,
            lastname=lastname,
            username=username,
            documentType_id=documentType_id,
            identification=identification,
            password=password,
            userType_id=userType_id
        )
        validation = validator.validateUserData(new_user)
        if validation["isValid"]:
            db.session.add(new_user)
            db.session.commit()
        self.log.info(validation["response"])
        return validation["response"]
    


class User(Resource):
    @jwt_required()
    def get(self, id_user):
        return user_schema.dump(ApplicationUser.query.get_or_404(id_user))
    
    @jwt_required()
    def put(self, id_user):
        user = ApplicationUser.query.filter(ApplicationUser.id==id_user).first()
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
        if validation["isValid"]:
            db.session.commit()
        self.log.info(validation["response"])
        return validation["response"]


        