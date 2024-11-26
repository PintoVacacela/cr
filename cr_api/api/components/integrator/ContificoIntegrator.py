import requests
import json
from ...model import *
import traceback

class ContificoIntegrator ():

    def __init__(self):
        with open('api/utilities/contifico/config_test.json') as arch:
                self.contifico_config = json.load(arch)
        self.path = self.contifico_config["contifico_url"]
        self.key = self.contifico_config["contifico_key"]
        self.token = self.contifico_config["contifico_token"]
        self.header = {
                "Authorization":self.key
                }
        
    def getAtribute(self,attr):
        if attr == "path":
            return self.path
        if attr == "key":
            return self.key
        if attr == "token":
            return self.token
        return None


    def getClientData(self):
        try:
            clients = requests.get(self.path+"/persona/", headers=self.header)
            clients_json=clients.json()
            return clients_json
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        
    def getProductsData(self):
        try:
            products = requests.get(self.path+"/producto/", headers=self.header)
            products_json=products.json()
            return products_json
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        
    def createBill(self, bill):
        try:
            response = requests.get(self.path+"/producto/",json=bill, headers=self.header)
            response=response.json()
            return bill
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None

         