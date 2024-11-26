from ..logic.ModelManager import *
from ...model.product import *
from sqlalchemy.orm import aliased
from sqlalchemy import case
import requests
from flask import jsonify
from ..integrator.ContificoIntegrator import *


class ProductManager (ModelManager):

    def __init__(self):
        super().__init__(Product)
        with open('api/utilities/contifico/config.json') as arch:
                self.contifico_config = json.load(arch)
        self.path = self.contifico_config["contifico_url"]
        self.key = self.contifico_config["contifico_key"]


    def getProductData(self):
        try:
            integrator = ContificoIntegrator()
            
            products_json=integrator.getProductsData()
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
        
    
    def findProductsPerType(self, type):
        try:
            products = self.model.query.filter(self.model.type==type).all()
            return products
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None
        
    def findProductsAndAssignments(self,id_client):
        try:
            sql_query = """SELECT 
                                p.id,
                                p.code,
                                p.name,
                                p.pvp1,
                                p.pvp2,
                                p.pvp3,
                                
                                CASE
                                    WHEN pa.value IS NOT NULL THEN pa.value 
                                    ELSE p.pvp1                               
                                END AS price
                            FROM 
                                Product p
                            LEFT JOIN 
                                product_assignment pa ON pa.product_id = p.id 
                                AND pa.client_id = :id_client"""

            # Ejecutar el query y obtener los resultados
            results = db.session.execute(sql_query, {'id_client': id_client}).fetchall()
            result_data = []
            for result in results:
                result_data.append({
                    'id': result.id,
                    'code': result.code,
                    'name': result.name,
                    'pvp1': result.pvp1,
                    'pvp2': result.pvp2,
                    'pvp3': result.pvp3,
                    'price': result.price  # Este es el valor calculado para el precio
                })

            # Paso 3: Convertir a JSON (puedes usar jsonify si lo quieres enviar como respuesta HTTP)
            response = jsonify(result_data)
            return response
        except Exception as e:
            self.log.errorExc(None,e,traceback)
            return None



    