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
validator = ClientValidation()


class ContificoClientsView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager = ClientManager()

    @jwt_required()
    def get(self):
        clients = self.manager.getClientData()
        if clients:
            return clients,200
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
        id_client=request.form.get("id_client")
        ruc=request.form.get("ruc")
        cedula=request.form.get("cedula")
        placa=request.form.get("placa")
        razon_social=request.form.get("razon_social")
        telefonos=request.form.get("telefonos")
        direccion=request.form.get("direccion")
        tipo=request.form.get("tipo")
        es_cliente=request.form.get("es_cliente")
        es_proveedor=request.form.get("es_proveedor")
        es_empleado=request.form.get("es_empleado")
        es_corporativo=request.form.get("es_corporativo")
        aplicar_cupo=request.form.get("aplicar_cupo")
        email=request.form.get("email")
        es_vendedor=request.form.get("es_vendedor")
        es_extranjero=request.form.get("es_extranjero")
        porcentaje_descuento=request.form.get("porcentaje_descuento")
        banco_codigo_id=request.form.get("banco_codigo_id")
        tipo_cuenta=request.form.get("tipo_cuenta")
        numero_tarjeta=request.form.get("numero_tarjeta")
        personaasociada_id=request.form.get("personaasociada_id")
        nombre_comercial=request.form.get("nombre_comercial")
        origen=request.form.get("origen")
        pvp_default=request.form.get("pvp_default")
        id_categoria=request.form.get("id_categoria")
        categoria_nombre=request.form.get("categoria_nombre")
        
        new_client = Client(
            id_client=id_client,
            ruc=ruc,
            cedula=cedula,
            placa=placa,
            razon_social=razon_social,
            telefonos=telefonos,
            direccion=direccion,
            tipo=tipo,
            es_cliente=es_cliente,
            es_proveedor=es_proveedor,
            es_empleado=es_empleado,
            es_corporativo=es_corporativo,
            aplicar_cupo=aplicar_cupo,
            email=email,
            es_vendedor=es_vendedor,
            es_extranjero=es_extranjero,
            porcentaje_descuento=porcentaje_descuento,
            banco_codigo_id=banco_codigo_id,
            tipo_cuenta=tipo_cuenta,
            numero_tarjeta=numero_tarjeta,
            personaasociada_id=personaasociada_id,
            nombre_comercial=nombre_comercial,
            origen=origen,
            pvp_default=pvp_default,
            id_categoria=id_categoria,
            categoria_nombre=categoria_nombre
        )
        
        validation = validator.validateClientData(new_client)
        if validation.isValid:
            self.manager.create(new_client)
            self.log.info(acces_id,validation.response)
            return response_util.performResponseObject(201,"Cliente creado exitosamente!",client_schema.dump(new_client))
        else:
            response = response_util.performResponse(400,validation.response)
        self.log.error(acces_id,validation.response)
        return response
                