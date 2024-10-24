from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

socketio = None  # Inicialización tardía

user_sockets = {}  # Almacena la relación entre usuario y su socket

def init_socketio(sio: SocketIO):
    global socketio
    socketio = sio

    @socketio.on('connect')
    @jwt_required()
    def handle_connect():
        current_user = get_jwt_identity()
        join_room(current_user)
        print(f'User connected: {current_user}')

    @socketio.on('send_notification')
    @jwt_required()
    def handle_send_notification(data):
        current_user = get_jwt_identity()
        recipient = current_user  # Usuario destinatario
        message = data.get('message')
        
        # Envía la notificación solo al destinatario específico
        emit_notification_to_user(current_user,message)
        print(f'Notification from {current_user} to {recipient}: {message}')


    @socketio.on('disconnect')
    @jwt_required()
    def handle_disconnect():
        current_user = get_jwt_identity()
        leave_room(current_user)  # Salir de la sala del usuario
        print(f'User disconnected: {current_user}')


def emit_notification_to_user(user_id, data):
    socketio.emit('receive_notification', data, room=user_id)

def emit_alert_to_user(user_id, data):
    socketio.emit('receive_alert', data, room=user_id)
