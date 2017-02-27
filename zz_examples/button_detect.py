import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    print("Waiting....")
    GPIO.wait_for_edge(24, GPIO.RISING)
    print("Button pressed")
    GPIO.wait_for_edge(24, GPIO.FALLING)
    print("Button Released")

GPIO.cleanup()
