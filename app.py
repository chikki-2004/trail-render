from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join-room')
def handle_join(data):
    room = data['room']
    socketio.join_room(room)
    socketio.emit('user-connected', {'userId': data['userId']}, to=room)

@socketio.on('signal')
def handle_signal(data):
    socketio.emit('signal', data, to=data['room'])

@socketio.on('disconnect')
def handle_disconnect():
    socketio.emit('user-disconnected', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
