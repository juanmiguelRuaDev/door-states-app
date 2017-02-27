import RPi.GPIO as GPIO
import time
pin = 16 
delay = 0.25
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)
for i in range(1,10):
        GPIO.setup(pin, GPIO.IN)
        time.sleep(delay)
        GPIO.setup(pin, GPIO.OUT)
        time.sleep(delay)
GPIO.cleanup()
