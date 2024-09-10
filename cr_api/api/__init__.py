from flask import Flask
import json

def create_app():
    app = Flask(__name__)

    with open('credentials.json') as arch:
        config = json.load(arch)

    conexion = 'mssql+pyodbc://' + config['user']+ ':' + config['password'] + '@' + config['host'] + '/' + config['database']+'?driver=ODBC+Driver+17+for+SQL+Server' 
    app.config['SQLALCHEMY_DATABASE_URI'] = conexion
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fa'
    app.config['JWT_SECRET_KEY']='Maestría-en-Ingeniería-de-Software-Miso2022'
    app.config['PROPAGATE_EXCEPTIONS'] = True

    return app
