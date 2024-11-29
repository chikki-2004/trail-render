from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join-room')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('user-connected', {'userId': data['userId']}, to=room)

@socketio.on('signal')
def handle_signal(data):
    emit('signal', data, to=data['room'])

@socketio.on('disconnect')
def handle_disconnect():
    emit('user-disconnected', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
