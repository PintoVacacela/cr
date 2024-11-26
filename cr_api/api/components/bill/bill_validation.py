from ...model.user import *
from ...model.profile import *
from ...utilities.responses import *
from ...utilities.loger import *
from .BillManager import *



response_util = WebResponse()


class BillValidation:
     
    @staticmethod
    def validateBillData(bill: Bill):
        response = any
        isValid = False
        if  FormatValidator.isNullOrEmpty(bill.client_id):
            response = "No se ha seleccionado un cliente!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(bill.document):
            response = "Numero de documento inválido!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(bill.description):
            response = "Descripción de documento inválido!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(bill.iva):
            response = "IVA de documento inválido!"
            return ValidationResponse(isValid,response)
        if FormatValidator.isNullOrEmpty(bill.total):
            response = "NuTotal de documento inválido!"
            return ValidationResponse(isValid,response)
        if bill.issue_date is None:
            response = "Fecha invalida!"
            return ValidationResponse(isValid,response)
        if not FormatValidator.validateDateFormat(bill.issue_date):
            response = "Formato Fecha invalido!"
            return ValidationResponse(isValid,response)
        isValid = True
        response = "Success!"
        return ValidationResponse(isValid,response)
    

    @staticmethod 
    def validateDeleteBill(bill: Bill):
        if bill.is_sended:
            isValid = False
            response = "Documento ya enviado, no se puede actualizar ni eliminar!"
            return ValidationResponse(isValid,response)
        isValid = True
        response = "Success!"
        
        return ValidationResponse(isValid,response)
    
    