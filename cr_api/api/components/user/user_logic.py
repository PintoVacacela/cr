from flask import request
from flask_restful import Resource
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from statistics import mean
from ...model.user import *



user_schema = UserSchema()



def ValidarEmail(email: str) -> tuple:
    if email is not None:
        try:
            valid = validate_email(email)
            email = valid.email
            return True, email
        except EmailNotValidError as e:
            return False, str(e)
   


class Register(Resource):
    def get(self):
        return {'mesage':'Ok!'}, 200
        
    def post(self):
        email = request.json["email"]  
        password = request.json["password"]  
        nuevo_usuario = ApplicationUser(
            email=email,
            password=password
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return "Usuario Registrado exitosamente", 200
    
    

class Users(Resource):
    def get(self):
        users = ApplicationUser.query.all()
        return [user_schema.dump(user) for user in users]


class User(Resource):

    def get(self, id_user):
        return user_schema.dump(ApplicationUser.query.get_or_404(id_user))


        