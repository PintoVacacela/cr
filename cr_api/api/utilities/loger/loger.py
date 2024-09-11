import logging
from ..customized import *

class LoggerFactory:
    _instance = None 
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoggerFactory, cls).__new__(cls, *args, **kwargs)
            # Initialize any additional attributes if needed
        return cls._instance

    def __init__(self):
        self.loggers = SingletonList()

    
    def get_logger(self, clazz):
        
        for obj in self.loggers.get_list():
            if obj["class"] == clazz:
                return obj["logger"]
        new_logger = Logger(clazz)
        self.loggers.add_item({'class':clazz,'logger':new_logger})
        return new_logger
        

class Logger:

    def __init__(self, clazz):
        self.clazz = clazz
        self.logger = logging.getLogger(clazz.__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # Create a file handler
        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(logging.INFO)
        
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        
        # Create a formatter and set it for the handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logger.propagate = False
        
    
    def info(self, user, msg):
        self.logger.info(f"User: {user} On: {self.clazz} : {msg}")

        
    
    def errorExc(self, user, exc:str, traceback:any):
        trace = any
        if exc is None:
            exc = 'Not found exception'

        if traceback is None:
            trace = 'Not found traceback'
        else:
            trace = traceback.format_exc()
        self.logger.error(f"User: {user} On: {self.clazz} : An error occurred: {exc} : {trace}")


    def errorInfo(self, user, msg:str):
        if exc is None:
            exc = 'Not found exception'
        self.logger.error(f"User: {user} On: {self.clazz} : {msg}")
    



