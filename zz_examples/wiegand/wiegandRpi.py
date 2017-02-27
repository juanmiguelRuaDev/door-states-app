#!/usr/bin/env python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # data 0
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # data 1


def main():
    x = 1
    bit = 0
    d0 = 0
    d1 = 0
    while True:
        d0 = GPIO.input(20)
        d1 = GPIO.input(21)
        if d0 == 0:
            bit = 0
        if d1 == 0:
            bit = 1
        print("Bit %s: %s" % (x, bit))
        x += 1


if __name__ == '__main__':
    main()
