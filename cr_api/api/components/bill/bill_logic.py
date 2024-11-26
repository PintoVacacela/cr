from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity

from ...utilities.responses import *
from ...utilities.loger import *

from ...schemas.model_schema import *
from .BillManager import * 
from .bill_validation import *
from ..integrator.ContificoIntegrator import *

bill_schema = BillSchema()
validator = BillValidation()

def sendDocument(bill:Bill):
    
    integrator = ContificoIntegrator()

    details = []

    for detail in bill.details:
        det = {
            "producto_id": detail.product.id_product,
            "cantidad": detail.quantity,
            "precio": detail.price,
            "porcentaje_iva": detail.iva,
            "porcentaje_descuento": detail.discount,
            "base_cero":detail.quantity,
            "base_gravable": detail.price,
            "base_no_gravable": detail.quantity
        }
        details.append(det)

    obj_json = {
    "pos" : integrator.getAtribute("token"),
    "fecha_emision": bill.issue_date,
    "tipo_documento": bill.document_type,
    "autorizacion": "",
    "documento": bill.document,
    "cliente": {
        "ruc": bill.client.ruc,
        "cedula": bill.client.identification,
        "razon_social": bill.client.identification,
        "telefonos": "11111111",
        "direccion": "AV. 99 DE OCTUBRE 729 Y BOYACA - GARCIA AVILES",
        "tipo": bill.client.type,
        "email": bill.client.email,
        "es_extranjero": bill.client.is_foreign
    },
    "descripcion": bill.description,
    "subtotal_0": bill.subtotal_0,
    "subtotal_12": bill.subtotal_12,
    "iva": bill.iva,
    "ice": 0.00,
    "servicio": 0.00,
    "total": bill.total,
    "adicional1": "",
    "adicional2": "",
    "detalles": details
}
    response = integrator.createBill(obj_json)
    return response

class BillsClientView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager= BillManager()

class BillsView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
        self.manager= BillManager()

    
    @jwt_required()
    def get(self, id_bill):
        bills = self.manager.findClientBills(id_bill)
        return [bill_schema.dump(item) for item in bills],200
    
    @jwt_required()
    def post(self):
        acces_id = get_jwt_identity()
        client_id = FormatValidator.getStrData(request.form.get("client_id"))
        issue_date = FormatValidator.getStrData(request.form.get("issue_date"))
        document = FormatValidator.getStrData(request.form.get("document"))
        seller_id = FormatValidator.getStrData(request.form.get("seller_id"))
        description = FormatValidator.getStrData(request.form.get("description"))
        subtotal15 = FormatValidator.getStrData(request.form.get("subtotal15"))
        subtotal5 = FormatValidator.getStrData(request.form.get("subtotal5"))
        subtotal0 = FormatValidator.getStrData(request.form.get("subtotal0"))
        discount = FormatValidator.getStrData(request.form.get("discount"))
        iva15 = FormatValidator.getStrData(request.form.get("iva15"))
        iva5 = FormatValidator.getStrData(request.form.get("iva5"))
        total = FormatValidator.getStrData(request.form.get("total"))
        details = FormatValidator.getStrData(request.form.get("details"))

        sendDocument = FormatValidator.getBooleanFromString(request.form.get("send"))
        
        new_bill = Bill(
            issue_date= issue_date,
            document= document,
            client_id= client_id,
            description= description,
            subtotal_0= subtotal0,
            subtotal_12= subtotal15,
            iva= iva15,
            total= total,
            seller_id= seller_id,

        )
        response = any

        if not details:
            return response_util.performResponse(400,"No existe ningun detalle!")

        validation = validator.validateBillData(new_bill)
        if validation.isValid:
            self.manager.create(new_bill)
            print(new_bill.id)
            data = FormatValidator.getObjectFromRquestJson(details)
            self.manager.appendDetails(new_bill.id,data)
            message = "Documento creado exitosamente!"
            if sendDocument:
                resp = sendDocument(new_bill)
                if resp is not None:
                    message = "Documento creado y enviado exitosamente!" 
                    new_bill.is_sended = True
                    self.manager.put()

            self.log.info(acces_id,validation.response)
            return response_util.performResponseObject(201,message,bill_schema.dump(new_bill))
        else:
            response = response_util.performResponse(400,validation.response)
        
        self.log.error(acces_id,validation.response)
        return response
    
class BillView(Resource):
    def __init__(self): 
        self.manager = BillManager()
        self.log = LoggerFactory().get_logger(self.__class__)

    @jwt_required()
    def get(self, id_bill):
        return bill_schema.dump(self.manager.findById(id_bill))
    
    @jwt_required()
    def delete(self, id_bill):
        acces_id = get_jwt_identity()
        bill = self.manager.findById(id_bill)
        validation = validator.validateDeleteBill(bill)
        if not validation.isValid:
            return response_util.performResponse(404,validation.response)
        if bill is None:
            return response_util.performResponse(404,"No se puede encontrar el documento!")
        bill.details.clear()
        self.manager.delete(bill)
        response = response_util.performResponse(201,"Documento eliminado exitosamente!")
        self.log.info(acces_id,response)
        return response
    
    @jwt_required()
    def put(self, id_bill):
        acces_id = get_jwt_identity()
        bill = self.manager.findById(id_bill)
        if bill is None:
            return response_util.performResponse(404,"No se puede encontrar el documento!")
        
        validation = validator.validateDeleteBill(bill)
        if not validation.isValid:
            return response_util.performResponse(404,validation.response)

        client_id = FormatValidator.getStrData(request.form.get("client_id"))
        issue_date = FormatValidator.getStrData(request.form.get("issue_date"))
        document = FormatValidator.getStrData(request.form.get("document"))
        seller_id = FormatValidator.getStrData(request.form.get("seller_id"))
        description = FormatValidator.getStrData(request.form.get("description"))
        subtotal15 = FormatValidator.getStrData(request.form.get("subtotal15"))
        subtotal5 = FormatValidator.getStrData(request.form.get("subtotal5"))
        subtotal0 = FormatValidator.getStrData(request.form.get("subtotal0"))
        discount = FormatValidator.getStrData(request.form.get("discount"))
        iva15 = FormatValidator.getStrData(request.form.get("iva15"))
        iva5 = FormatValidator.getStrData(request.form.get("iva5"))
        total = FormatValidator.getStrData(request.form.get("total"))

        details = FormatValidator.getStrData(request.form.get("details"))

        sendDocument = FormatValidator.getBooleanFromString(request.form.get("send"))

        bill.issue_date= issue_date
        bill.document= document
        bill.client_id= client_id
        bill.description= description
        bill.subtotal_0= subtotal0
        bill.subtotal_12= subtotal15
        bill.iva= iva15
        bill.total= total
        bill.seller_id= seller_id
        
        validation = validator.validateBillData(bill)
        if not details:
            return response_util.performResponse(400,"No existe ningun detalle!")

        if validation.isValid:
            self.manager.put()
            data = FormatValidator.getObjectFromRquestJson(details)
            self.manager.appendDetails(bill.id,data)
            message = "Documento actualizado exitosamente!"
            if sendDocument:
                resp = sendDocument(bill)
                if resp is not None:
                    message = "Documento actualizado y enviado exitosamente!" 
                    bill.is_sended = True
                    self.manager.put()
            self.log.info(acces_id,validation.response)
            return response_util.performResponseObject(201,message,bill_schema.dump(bill))
            
        else:
            self.log.error(acces_id,validation.response)
        return response_util.performResponse(400,validation.response)
    

    


    