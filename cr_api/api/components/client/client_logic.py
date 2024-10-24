from flask import request
from flask_restful import Resource
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from ...model.client import *
from ...utilities.responses import *
from ...utilities.loger import *
from .ClientManager import *
from ...schemas.model_schema import *
from .client_validation import *


client_schema = ClientSchema()
validator = ClientValidator()


class ContificoClientsView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ClientManager()

    @jwt_required()
    def get(self):
        clients = self.manager.getClientData()
        if clients:
            return True,200
        return response_util.performResponse(404,"No se pudo obtener la lista!")


class PaymentTypeView(Resource):
    @jwt_required()
    def get(self):
        obj = []
        for k in PaymentType:
            obj.append({"key":k.name, "value":k.value})
        return obj
    
class ClientTypeView(Resource):
    @jwt_required()
    def get(self):
        obj = []
        for k in ClientType:
            obj.append({"key":k.name, "value":k.value})
        return obj


class ClientsView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ClientManager()

    @jwt_required()
    def get(self):
        clients = self.manager.findAll()
        return [client_schema.dump(item) for item in clients],200
    
    @jwt_required()
    def post(self):
        acces_id = get_jwt_identity()
        type=FormatValidator.getStrData(request.form.get("type"))
        ruc=FormatValidator.getStrData(request.form.get("ruc"))
        identification=FormatValidator.getStrData(request.form.get("identification"))
        name=FormatValidator.getStrData(request.form.get("name"))
        comercial_name=FormatValidator.getStrData(request.form.get("comercial_name"))
        province=FormatValidator.getStrData(request.form.get("province"))
        canton=FormatValidator.getStrData(request.form.get("canton"))
        parish=FormatValidator.getStrData(request.form.get("parish"))
        sex=FormatValidator.getStrData(request.form.get("sex"))
        civil_state=FormatValidator.getStrData(request.form.get("civil_state"))
        source_income=FormatValidator.getStrData(request.form.get("source_income"))
        is_foreign=FormatValidator.getBooleanFromString(request.form.get("is_foreign"))
        special_taxpayer=FormatValidator.getBooleanFromString(request.form.get("special_taxpayer"))
        email=FormatValidator.getStrData(request.form.get("email"))
        category_id=FormatValidator.getStrData(request.form.get("category_id"))
        new_client = Client(
            type=type,
            ruc=ruc,
            identification=identification,
            name=name,
            comercial_name=comercial_name,
            province=province,
            canton=canton,
            parish=parish,
            sex=sex,
            civil_state=civil_state,
            source_income=source_income,
            is_foreign=is_foreign,
            special_taxpayer=special_taxpayer,
            email=email,
            category_id=category_id
        )
        validation = validator.validateClientData(new_client)
        if not validation.isValid:
            response = response_util.performResponse(400,validation.response)
            self.log.error(acces_id,validation.response)
            return response
        self.manager.create(new_client)
        paymentType=FormatValidator.getStrData(request.form.get("paymentType"))
        paymentDays=FormatValidator.getStrData(request.form.get("paymentDays"))
        paymentMaxAmount=FormatValidator.getStrData(request.form.get("paymentMaxAmount"))
        if not paymentType:
            response = response_util.performResponse(400,"Se debe asignar un metodo de pago!")
            self.log.error(acces_id,validation.response)
            return response
        else :
            new_payment = PaymentMethod(
                type=paymentType,
                days=paymentDays,
                max_amount=paymentMaxAmount,
                client_id=new_client.id
            )
            
            payment_manager = ModelManager(PaymentMethod)
            payment_manager.create(new_payment)

        contacts=FormatValidator.getStrData(request.form.get("contacts"))
        addresses=FormatValidator.getStrData(request.form.get("addresses"))

        if contacts:
            data = FormatValidator.getObjectFromRquestJson(contacts)
            self.manager.appendContacts(new_client,data)
        
        if addresses:
            data = FormatValidator.getObjectFromRquestJson(addresses)
            self.manager.appendAddresses(new_client,data)

        self.log.info(acces_id,validation.response)
        return response_util.performResponseObject(201,"Cliente creado exitosamente!",client_schema.dump(new_client))
      

class ClientView(Resource):
    def __init__(self):
        self.manager = ClientManager()
        self.log = LoggerFactory().get_logger(self.__class__)

    @jwt_required()
    def get(self, id_client):
        return client_schema.dump(self.manager.findById(id_client))
    
    @jwt_required()
    def delete(self, id_client):
        acces_id = get_jwt_identity()
        client = self.manager.findById(id_client)
        if client is None:
            return response_util.performResponse(404,"No se puede encontrar el cliente!")
        validation = validator.validateDeleteClient(client)
        if not validation.isValid:
            return response_util.performResponse(404,validation.response)
        self.manager.delete(client)
        response = response_util.performResponse(201,"Cliente eliminado exitosamente!")
        self.log.info(acces_id,response)
        return response

    
    @jwt_required()
    def put(self, id_client):
        acces_id = get_jwt_identity()
        client = self.manager.findById(id_client)
        if client is None:
            return response_util.performResponse(404,"No se puede encontrar el cliente!")

        type=FormatValidator.getStrData(request.form.get("type"))
        ruc=FormatValidator.getStrData(request.form.get("ruc"))
        identification=FormatValidator.getStrData(request.form.get("identification"))
        name=FormatValidator.getStrData(request.form.get("name"))
        comercial_name=FormatValidator.getStrData(request.form.get("comercial_name"))
        province=FormatValidator.getStrData(request.form.get("province"))
        canton=FormatValidator.getStrData(request.form.get("canton"))
        parish=FormatValidator.getStrData(request.form.get("parish"))
        sex=FormatValidator.getStrData(request.form.get("sex"))
        civil_state=FormatValidator.getStrData(request.form.get("civil_state"))
        source_income=FormatValidator.getStrData(request.form.get("source_income"))
        is_foreign=FormatValidator.getBooleanFromString(request.form.get("is_foreign"))
        special_taxpayer=FormatValidator.getBooleanFromString(request.form.get("special_taxpayer"))
        email=FormatValidator.getStrData(request.form.get("email"))
        category_id=FormatValidator.getStrData(request.form.get("category_id"))

        client.type = type
        client.ruc = ruc
        client.identification = identification
        client.name = name
        client.comercial_name = comercial_name
        client.province = province
        client.canton = canton
        client.parish = parish
        client.sex = sex
        client.civil_state = civil_state
        client.source_income = source_income
        client.is_foreign = is_foreign
        client.special_taxpayer = special_taxpayer
        client.email = email
        client.category_id = category_id
        
        validation = validator.validateClientData(client)
        if not validation.isValid:
            response = response_util.performResponse(400,validation.response)
            self.log.error(acces_id,validation.response)
            return response
        self.manager.put()
        paymentType=FormatValidator.getStrData(request.form.get("paymentType"))
        paymentDays=FormatValidator.getStrData(request.form.get("paymentDays"))
        paymentMaxAmount=FormatValidator.getStrData(request.form.get("paymentMaxAmount"))
        if not paymentType:
            response = response_util.performResponse(400,"Se debe asignar un metodo de pago!")
            self.log.error(acces_id,validation.response)
            return response
        else :
            payment = PaymentMethod.query.filter(PaymentMethod.client_id == client.id).first()
            payment.type=paymentType
            payment.days=paymentDays
            payment.max_amount=paymentMaxAmount
            self.manager.put()

        contacts=FormatValidator.getStrData(request.form.get("contacts"))
        addresses=FormatValidator.getStrData(request.form.get("addresses"))

        if contacts:
            data = FormatValidator.getObjectFromRquestJson(contacts)
            self.manager.appendContacts(client,data)
        
        if addresses:
            data = FormatValidator.getObjectFromRquestJson(addresses)
            self.manager.appendAddresses(client,data)
        return response_util.performResponseObject(200,"Cliente actualizado exitosamente!", client_schema.dump(client))