import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def rising_callback(channel):
    print("Rising")


def falling_callback(channel):
    print("Falling")

GPIO.add_event_detect(24, GPIO.RISING, callback=rising_callback)
GPIO.add_event_detect(23, GPIO.FALLING, callback=falling_callback)

try:
    while True:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
