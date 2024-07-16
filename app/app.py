import RPi.GPIO as GPIO
import time
import requests

LED = 13
BUTTON = 15

print("Starting GPIO Pin Configuration...")
GPIO.setmode(GPIO.BOARD)

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.OUT)
print("GPIO Pin Configured")
while True:
    try:    
        print("Requesting the server...", end="", sep="")
        answer = requests.get("http://172.20.10.3:5000/get_press").json()
        status = int(answer["led_status"])
        print(f"Success! Got {status}.", end="", sep="")
        button = GPIO.input(BUTTON)
        print(f"|| Status of the button: {button}", end="", sep="")
        print()
        if button == 0 and status == 0:
            GPIO.output(LED, GPIO.LOW)
        elif status == 1:
            GPIO.output(LED, GPIO.HIGH)
        requests.post("http://172.20.10.3:5000/press", json={
            "id": 0,
            "status": button
        })
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(0.1)

GPIO.cleanup()