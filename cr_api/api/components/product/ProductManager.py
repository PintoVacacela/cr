from ..logic.ModelManager import *
from ...model.product import *
import requests


class ProductManager (ModelManager):

    def __init__(self):
        super().__init__(Product)
        with open('api/utilities/contifico/config.json') as arch:
                self.contifico_config = json.load(arch)
        self.path = self.contifico_config["contifico_url"]
        self.key = self.contifico_config["contifico_key"]


    def getProductData(self):
        try:
            headers = {
                "Authorization":self.key
                }
            products = requests.get(self.path+"/producto/", headers=headers)
            products_json=products.json()
            db.session.query(self.model).delete()
            db.session.commit()
            for product in products_json:
                 new_client = Product(
                        id_product = product.get("id"),
                        code = product.get("codigo"),
                        product_type = product.get("tipo_producto"),
                        for_pos = product.get("para_pos"),
                        name = product.get("nombre"),
                        barcode = product.get("codigo_barra"),
                        category_id = product.get("categoria_id"),
                        brand_id = product.get("marca_id"),
                        brand_name = product.get("marca_nombre"),
                        vat_percentage = product.get("porcentaje_iva"),
                        pvp1 = product.get("pvp1"),
                        pvp2 = product.get("pvp2"),
                        pvp3 = product.get("pvp3"),
                        pvp4 = product.get("pvp4"),
                        minimum = product.get("minimo"),
                        stock_quantity = product.get("cantidad_stock"),
                        manual_pvp = product.get("pvp_manual"),
                        image = product.get("imagen"),
                        description = product.get("descripcion"),
                        type = product.get("tipo"),
                        max_cost = product.get("costo_maximo"),
                        creation_date = product.get("fecha_creacion"),
                        supplier_code = product.get("codigo_proveedor"),
                        lead_time = product.get("lead_time"),
                        automatic_generation = product.get("generacion_automatica")
                 )
                 db.session.add(new_client)
            db.session.commit()
            return True
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return False
        
    




    