from flask import request
from flask_restful import Resource
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from ...model.client import *
from ...utilities.responses import *
from ...utilities.loger import *
from .ClientManager import *


user_schema = ClientSchema()



class Clients(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ClientManager()

    
    def get(self):
        clients = self.manager.getClientData()
        return clients,200
    
    