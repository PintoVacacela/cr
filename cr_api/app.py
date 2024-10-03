from api import create_app
from api.model import db
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS
from api.components.user.user_logic import *
from api.components.client.client_logic import *
from api.components.menu.menu_logic import *
from api.components.profile.profile_logic import *
from api.utilities.uploaded_files import *
from api import UPLOAD_FOLDER
from flask_socketio import SocketIO, emit
from api.utilities.notifications import register_socket_events
import os



app = create_app()
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)

api.add_resource(LoginView, '/api/login')
api.add_resource(UserConfigView, '/api/configure-user')

api.add_resource(UsersView, '/api/users')
api.add_resource(UserView, '/api/user/<string:id_user>')

api.add_resource(MenusView, '/api/menus')
api.add_resource(UserMenusView, '/api/user_menus')


api.add_resource(ProfilesView, '/api/profiles')
api.add_resource(ProfileView, '/api/profile/<string:id_profile>')

api.add_resource(DocumentTypesView, '/api/document_types')
api.add_resource(DocumentTypeView, '/api/document_type/<string:id_document>')

api.add_resource(UserTypesView, '/api/user_types')
api.add_resource(UserTypeView, '/api/user_type/<string:id_type>')

api.add_resource(ClientsView, '/api/clients')
api.add_resource(PaymentTypeView, '/api/payment_types')
api.add_resource(ClientTypeView, '/api/client_types')






api.add_resource(ContificoClientsView, '/api/contifico_clients')

socketio = SocketIO(app)


# api.add_resource(UploadView, '/uploads/<string:file_name>')

@app.route('/uploads/<path:filename>', methods=['GET'])
def uploaded_file(filename):
    print(filename)
    return send_from_directory(UPLOAD_FOLDER, filename)

@socketio.on('send_notification')
def handle_notification(data):
    # Enviar notificación a todos los clientes conectados
    emit('receive_notification', data, broadcast=True)

jwt = JWTManager(app)


if __name__ == "__main__":
    socketio.run(host='0.0.0.0')
