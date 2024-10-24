
import re
import json
from datetime import datetime

class FormatValidator:

    @staticmethod
    def isNullOrEmpty(data):
        if data is None or data.strip() == '' or data == 'null':
            return True
        return False
    
    @staticmethod
    def getStrData(data):
        if isinstance(data, str):
            if data is None or data.strip() == '' or data == 'null':
                return None
        return data
    
    import re

    @staticmethod
    def getListFomrString(data):
        if data is not None and data != "":
            # Limpia la cadena de corchetes, llaves y comillas
            cleaned_string = re.sub(r'[\[\]{}()]', '', data)  # Elimina corchetes y llaves
            cleaned_string = re.sub(r'["\']', '', cleaned_string)  # Elimina comillas simples y dobles
            
            # Divide la cadena en una lista
            transformed = cleaned_string.split(",")
            
            # Elimina espacios en blanco alrededor de cada elemento
            transformed = [item.strip() for item in transformed if item.strip()]
            
            return transformed
        return None

    
    @staticmethod
    def getObjectFromRquestJson(data_json):
        if data_json:
            array = json.loads(data_json)
            return array
        return None
    
    @staticmethod
    def getBooleanFromString(data):
        if data and data == 'true':
            return True
        return False
    
    @staticmethod
    def validateDateFormat(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d') 
            return True
        except ValueError:
            raise False
        
    @staticmethod
    def getDateFromString(date_string):
        cleaned_date_string = ' '.join(date_string.split()[:5])
        parsed_date = datetime.strptime(cleaned_date_string, '%a %b %d %Y %H:%M:%S').date()
        return parsed_date
    
    