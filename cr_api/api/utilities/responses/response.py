import json
from ..loger import *
import traceback

class WebResponse:

    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)


    def performResponse(self, code, message):
        data = self._getDataResponse(code)
        if data is not None:
            return {'code':code,
                    'message':message,
                    'description':data.get("description"),
                    'type':data.get("type")
                    }, code
        else:
            return {'message':message},code
    
    def performResponse(self, code, message, token):
        data = self._getDataResponse(code)
        if data is not None:
            return {'code':code,
                    'message':message,
                    'description':data.get("description"),
                    'type':data.get("type"),
                    'token':token
                    }, code
        else:
            return {'message':message},code
    
    def _getDataResponse(self, code):
        try:
            with open('api/utilities/responses/err_codes.json') as arch:
                resp = json.load(arch)
            for data in resp:
                if data["code"] == code:
                    return data["data"]
            return None
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
            
        

    