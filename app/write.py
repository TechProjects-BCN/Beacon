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
GPIO.output(BUTTON, GPIO.LOW)
while True:
    try:
        button = GPIO.input(BUTTON)
        if button:
            GPIO.output(LED, GPIO.HIGH)
        else: 
            GPIO.output(LED, GPIO.LOW)
        print(f"|| Status of the button: {button}", end="", sep="")
        print()
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(0.1)

GPIO.cleanup()