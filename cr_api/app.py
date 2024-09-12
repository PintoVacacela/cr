from api import create_app

from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS
from api.model import db
from api.components.user.user_logic import *
from api.components.client.client_logic import *


app = create_app()
app_context = app.app_context()
app_context.push()


db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)

api.add_resource(Login, '/api/login')
api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/user/<string:id_usuario>')
api.add_resource(Clients, '/api/clients')

jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
