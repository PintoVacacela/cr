
import re

class FormatValidator:

    @staticmethod
    def isNullOrEmpty(data):
        if data is None or data.strip() == '':
            return True
        return False
    
    @staticmethod
    def getListFomrString(data):
        if data is not None or data != "":
            cleaned_string = re.sub(r'[\[\]{}()]', '', data)
            transformed = cleaned_string.split(",")
            return transformed
        return None