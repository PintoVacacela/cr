from flask import send_from_directory,request
from flask_restful import Resource
from datetime import date
from random import randint
from flask import current_app
from werkzeug.utils import secure_filename
import os
import traceback
from ..loger import *
from ... import UPLOAD_FOLDER


class UploadUtils:
   
    @staticmethod
    def savePhoto(file,module):
            log = LoggerFactory().get_logger(__class__)
            try:
                
                prefix = f'{module}-{randint(10,900)}-{date.today()}'
                filename = secure_filename(file.filename)
                filename = f'{prefix}-{filename}'
                file.save(os.path.join(
                    UPLOAD_FOLDER,
                    filename
                ))
                image_url = request.host_url + 'uploads/' + filename
                return image_url 
        
            except Exception as e:
                log.errorExc(None,e,traceback)
                return None

    @staticmethod
    def delete_image(url):
        log = LoggerFactory().get_logger(__class__)
        try:
            split = url.split("/")
            filename = split[-1]
            os.remove(os.path.join(UPLOAD_FOLDER, filename))
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            log.errorExc(None,e,traceback)
            return False

class UploadView(Resource):
    def __init__(self):
        self.log = LoggerFactory().get_logger(self.__class__)
    

    def get(self,file_name):
        print(file_name)
        
        print(UPLOAD_FOLDER)
        return send_from_directory(UPLOAD_FOLDER, file_name)