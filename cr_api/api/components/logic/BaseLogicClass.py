from flask import request
from flask_restful import Resource
from ...utilities.responses import *
from ...utilities.loger import *
from .ModelManager import *

class BaseLogicClass(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ModelManager()