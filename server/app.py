from flask import Flask, render_template, request, Response
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms

button_status = [0, 0, 0, 0]
led_status = 0


app = Flask(__name__)
app.config["SECRET_KEY"] = "fejhwfjewlk"
socketio = SocketIO(app)
CORS(app)


@app.route("/")
def main_route():
    return render_template("index.html")

@socketio.on('connect')
def handle_message():
    """
    Name: Connect Event for WebSockets
    Usage: Used by all incoming connections via websockets for the initial handshake.
    """
    print(f"Connection {request.sid}")
    emit("connection", {"Connected": 0}, to=request.sid)


@socketio.on("mode")
def update_mode_socket(modes):
    """
    Name: Mode Change Event for WebSockets
    Usage: Used by all incoming connections via websockets to specify what data they want to subscribe to.
    """
    # For all specified modes
    for mode in modes:
        # Join the room with that name
        join_room(mode, request.sid)
    print(f"{request.sid} changes modes to {modes}, now is in {rooms(request.sid)}")
    send({"Mode": "Changed"})


@socketio.on('disconnect')
def disconnect():
    """
    Name: Disconnection Event for WebSockets
    Usage: Used by all websocket connections to communicate to the server it is disconnecting.
    """
    print("Disconnection")
    # For all rooms the connection was part of.
    for room in rooms(request.sid):
        # Unsubscribe
        leave_room(room, request.sid)
    send({"Disconnected": 0})

@socketio.on('msg')
def disconnect(message):
    global led_status, button_status
    """
    Name: Disconnection Event for WebSockets
    Usage: Used by all websocket connections to communicate to the server it is disconnecting.
    """
    button_id = message["id"]
    button_status[button_id] = message["status"]
    if any(button_status):
        led_status = 1
    else:
        led_status = 0
    print(button_status)
    emit({"led_status": led_status})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=False, allow_unsafe_werkzeug=True)
