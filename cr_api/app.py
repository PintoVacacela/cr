from api import create_app
from api.model import db
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS

from api.components.user.user_logic import *
from api.components.client.client_logic import *
from api.components.client.client_category_logic import *
from api.components.menu.menu_logic import *
from api.components.profile.profile_logic import *
from api.components.product.product_logic import *
from api.components.notification.notification_logic import *
from api.components.event.event_logic import * 
from api.components.service.service_logic import *

from api.utilities.uploaded_files import *

from api import UPLOAD_FOLDER
from flask_socketio import SocketIO
from api.utilities.socket.socket_events import init_socketio

import os



app = create_app()
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()


CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:4200"}})

api = Api(app)

api.add_resource(LoginView, '/api/login')
api.add_resource(UserConfigView, '/api/configure-user')

api.add_resource(UsersView, '/api/users')
api.add_resource(UsersActiveView, '/api/users-active')
api.add_resource(UserView, '/api/user/<string:id_user>')

api.add_resource(NotificationsView, '/api/notifications')
api.add_resource(NotificationsAllView, '/api/notifications_all')
api.add_resource(NotificationView, '/api/notification/<string:id_notification>')

api.add_resource(MenusView, '/api/menus')
api.add_resource(UserMenusView, '/api/user_menus')


api.add_resource(ProfilesView, '/api/profiles')
api.add_resource(ProfileView, '/api/profile/<string:id_profile>')

api.add_resource(DocumentTypesView, '/api/document_types')
api.add_resource(DocumentTypeView, '/api/document_type/<string:id_document>')

api.add_resource(UserTypesView, '/api/user_types')
api.add_resource(UserTypeView, '/api/user_type/<string:id_type>')

api.add_resource(ClientsView, '/api/clients')
api.add_resource(ClientView, '/api/client/<string:id_client>')

api.add_resource(PaymentTypeView, '/api/payment_types')
api.add_resource(ClientTypeView, '/api/client_types')
api.add_resource(ClientCategorysView, '/api/client_categorys')
api.add_resource(ClientCategoryView, '/api/client_category/<string:id_category>')
api.add_resource(ClientCategoryTreeView, '/api/client_category_tree')
api.add_resource(ContificoClientsView, '/api/contifico_clients')

api.add_resource(EventsView, '/api/events')
api.add_resource(EventView, '/api/event/<string:id_event>')
api.add_resource(FrecuencyTypeView, '/api/frequency_types')
api.add_resource(EventTypeView, '/api/event_types')
api.add_resource(ScheduledEventsView, '/api/scheduled_events')




api.add_resource(ServicesView, '/api/services')
api.add_resource(ServiceView, '/api/service/<string:id_service>')

api.add_resource(ProductsView, '/api/products')

api.add_resource(ContificoProductsView, '/api/contifico_products')





socketio = SocketIO(app,  logger=False, engineio_logger=False,cors_allowed_origins=['http://localhost:4200'])


init_socketio(socketio)

@app.route('/uploads/<path:filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


jwt = JWTManager(app)


if __name__ == "__main__":
    socketio.run(host='0.0.0.0', port=5000)
