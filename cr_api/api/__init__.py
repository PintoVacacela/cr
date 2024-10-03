from flask import Flask
import json
import os

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def create_app():
    app = Flask(__name__)

    with open('credentials.json') as arch:
        config = json.load(arch)

    conexion = 'mssql+pyodbc://' + config['user']+ ':' + config['password'] + '@' + config['host'] + '/' + config['database']+'?driver=ODBC+Driver+17+for+SQL+Server' 
    app.config['SQLALCHEMY_DATABASE_URI'] = conexion
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY']='frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS'] = True

    
    return app


