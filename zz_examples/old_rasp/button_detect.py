import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

before = 0
after = 0


while True:
    input_state = GPIO.input(24)
    before = after
    if input_state == False:
        after = 1
        print('1')
    else:
        after = 0
        print('0')

    if before is 1 and after is 0:
        print('FALLING!!')

    if before is 0 and after is 1:
        print('...rising....')
    time.sleep(0.05)
