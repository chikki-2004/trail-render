from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

# Handle when a user joins the room
@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('joined', {'room': room}, room=room)  # Notify all peers in the room

# Handle WebRTC signaling messages (offer, answer, ice candidates)
@socketio.on('signal')
def handle_signal(data):
    room = data['room']
    message = data['message']
    # Emit the signaling message to all peers in the room, excluding the sender
    emit('signal', {'message': message}, room=room, include_self=False)

# Handle when a user leaves the room
@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    emit('left', {'room': room}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
