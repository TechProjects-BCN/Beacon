import RPi.GPIO as GPIO
import time
import socketio

sio = socketio.Client()

LED = 13
BUTTON = 15
URL = "http://172.20.10.3:5000"
status = 0
sio.connect(URL)

print("Starting GPIO Pin Configuration...")
GPIO.setmode(GPIO.BOARD)

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.OUT)
print("GPIO Pin Configured")

def startup(rq):
    time.sleep(1)
    sio.emit("mode", ["msg"])
    print('my sid is', sio.sid)

def callback(data):
    print(data)
    global answer, status
    answer = data
    try:
        status = int(answer["led_status"])
    except Exception as e:
        print(f"error: {e}")

previous = 0
change = True
sio.on("connection", startup)
startup({})
sio.on("msg", callback)

while True:
    try:
        button = GPIO.input(BUTTON)
        if button != previous:
            change = True
        print(f"Status of the button: {button} || Got: {status}")
        if button == 1:
            GPIO.output(LED, GPIO.HIGH)
            if change:
                sio.emit("msg", {
                "id": 0,
                "status": button
                })
                print("Sent Button Clicked")
                change = False
        if button == 0 and change:
            sio.emit("msg", {
                "id": 0,
                "status": button
                })
            change = False
            print("Sent Button Released")
        if button == 0 and status == 0:
            GPIO.output(LED, GPIO.LOW)
        elif status == 1:
            GPIO.output(LED, GPIO.HIGH)
        previous = button
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(0.05)

GPIO.cleanup()