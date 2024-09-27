from ..logic.ModelManager import *
from ...model.client import *
import requests


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
            headers = {
                "Authorization":self.key
                }
            clients = requests.get(self.path+"/persona/", headers=headers)
            clients_json=clients.json()
            db.session.query(self.model).delete()
            db.session.commit()
            for client in clients_json:
                 new_client = Client(
                        id=client.get("id"),
                        ruc=client.get("ruc"),
                        cedula=client.get("cedula"),
                        placa=client.get("placa"),
                        razon_social=client.get("razon_social"),
                        telefonos=client.get("telefonos"),
                        direccion=client.get("direccion"),
                        tipo=client.get("tipo"),
                        es_cliente=client.get("es_cliente"),
                        es_proveedor=client.get("es_proveedor"),
                        es_empleado=client.get("es_empleado"),
                        es_corporativo=client.get("es_corporativo"),
                        aplicar_cupo=client.get("aplicar_cupo"),
                        email=client.get("email"),
                        es_vendedor=client.get("es_vendedor"),
                        es_extranjero=client.get("es_extranjero"),
                        porcentaje_descuento=client.get("porcentaje_descuento"),
                        adicional1_cliente=client.get("adicional1_cliente"),
                        adicional2_cliente=client.get("adicional2_cliente"),
                        adicional3_cliente=client.get("adicional3_cliente"),
                        adicional4_cliente=client.get("adicional4_cliente"),
                        adicional1_proveedor=client.get("adicional1_proveedor"),
                        adicional2_proveedor=client.get("adicional2_proveedor"),
                        adicional3_proveedor=client.get("adicional3_proveedor"),
                        adicional4_proveedor=client.get("adicional4_proveedor"),
                        banco_codigo_id=client.get("banco_codigo_id"),
                        tipo_cuenta=client.get("tipo_cuenta"),
                        numero_tarjeta=client.get("numero_tarjeta"),
                        personaasociada_id=client.get("personaasociada_id"),
                        nombre_comercial=client.get("nombre_comercial"),
                        origen=client.get("origen"),
                        pvp_default=client.get("pvp_default"),
                        id_categoria=client.get("id_categoria"),
                        categoria_nombre=client.get("categoria_nombre")
                 )
                 db.session.add(new_client)
            db.session.commit()
            return True
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return False
        




    