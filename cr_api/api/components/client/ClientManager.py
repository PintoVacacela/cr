from ..logic.ModelManager import *
from ...model.client import *
from ..integrator.ContificoIntegrator import *


class ClientManager (ModelManager):

    def __init__(self):
        super().__init__(Client)
        with open('api/utilities/contifico/config.json') as arch:
                self.contifico_config = json.load(arch)
        self.path = self.contifico_config["contifico_url"]
        self.key = self.contifico_config["contifico_key"]

    def findRegisteredClient(self,cedula):
        try:
            search = self.model.query.filter(self.model.cedula == cedula).first()
            return search
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None

    def getClientData(self):
        try:
            integrator = ContificoIntegrator()
            clients_json=integrator.getClientData()
            db.session.query(self.model).delete()
            db.session.commit()
            for client in clients_json:
                 new_client = Client(
                        id_client=client.get("id"),
                        type=client.get("tipo"),
                        ruc=client.get("ruc"),
                        identification=client.get("cedula"),
                        name=client.get("razon_social"),
                        comercial_name=client.get("nombre_comercial"),
                        is_foreign=client.get("es_extranjero"),
                        email=client.get("email")
                 )
                 db.session.add(new_client)
            db.session.commit()
            return True
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return False
        
    def appendContacts(self,client:Client,contacts):
        try:   
            old_contacts = ContactInfo.query.filter(ContactInfo.client_id== client.id).all()
            for contact in contacts:
                if FormatValidator.getStrData(contact.get("id")) is None:
                    new_contact = ContactInfo(
                        area=contact.get("area"),
                        contact=contact.get("contact"),
                        client_id=client.id,
                        default=contact.get("default")
                    )
                    db.session.add(new_contact)
                    if new_contact.default:
                        client.default_phone = new_contact.contact
                else:
                    old_contact = next((old_contact for old_contact in old_contacts if old_contact.id == contact.get("id")), None)
                    if old_contact:
                        old_contact.area = contact.get("area")
                        old_contact.contact = contact.get("contact")
                        old_contact.default = contact.get("default")
                        db.session.commit()
                        old_contacts.remove(old_contact)
                        if old_contact.default:
                            client.default_phone = old_contact.contact
            for old in old_contacts:
                db.session.delete(old)
            db.session.commit()
            return client
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
                

    def appendAddresses(self,client:Client,addresses):
        try:   
            old_addresses = DeliveryAddress.query.filter(DeliveryAddress.client_id== client.id).all()
            for address in addresses:
                if FormatValidator.getStrData(address.get("id")) is None:
                    new_address = DeliveryAddress(
                        location=address.get("location"),
                        address=address.get("address"),
                        client_id=client.id,
                        default=address.get("default")
                    )
                    db.session.add(new_address)
                    if new_address.default:
                        client.default_address = new_address.address
                else:
                    old_address = next((old_address for old_address in old_addresses if old_address.id == address.get("id")), None)
                    if old_address:
                        old_address.location = address.get("location")
                        old_address.address = address.get("address")
                        old_address.default = address.get("default")
                        db.session.commit()
                        old_addresses.remove(old_address)
                        if old_address.default:
                            client.default_address = old_address.address
            for old in old_addresses:
                db.session.delete(old)
            db.session.commit()
            return client
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
    
    def delete(self,object):
        try:
            ContactInfo.query.filter(ContactInfo.client_id==object.id).delete()
            DeliveryAddress.query.filter(DeliveryAddress.client_id==object.id).delete()
            db.session.delete(object)
            db.session.commit()
            return True
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return False
        




    