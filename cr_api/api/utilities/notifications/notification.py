from flask_socketio import SocketIO

socketio = SocketIO()  # Crea una instancia de SocketIO

def register_socket_events(app):
    socketio.init_app(app)

    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('send_notification')
    def handle_notification(data):
        print('Received notification:', data)
        socketio.emit('receive_notification', data, broadcast=True)