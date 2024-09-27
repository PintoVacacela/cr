
class FormatValidator:

    @staticmethod
    def isNullOrEmpty(data):
        if data is None or data.strip() == '':
            return True
        return False