# -*- coding:utf -8-*-
from flask_socketio import join_room, emit
from backend import socketio


@socketio.on("enter room")
def handle_enter(json):
    room = json['uid']
    join_room(room)
    # emit('serverback', 'hi get you!', room=room)
