#!/usr/bin/env python
from time import sleep
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
# GPIO setup
data0 = 20
data1 = 21
GPIO.setup(data0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(data1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Variables
i = 0
dataBits = []
bitCount = 0
fcc = "0"
card = "0"
Zero = "0"
One = "1"
hexFilter = []
hexCard = []
hexFCC = []
justRead = 0
j = 0
k = 0
# Main code
while (1):
    # Reading code
    while bitCount <= 34:
        input0 = GPIO.input(data0)
        input1 = GPIO.input(data1)
        if input0 == 0 and input1 == 1:
            dataBits.append(Zero)
            print(dataBits)
            print("Bitcount %d" % bitCount)
            bitCount += 1
            justRead = 1
        if input1 == 0 and input0 == 1:
            dataBits.append(One)
            print(dataBits)
            print("Bitcount %d" % bitCount)
            bitCount += 1
            justRead = 1
        if bitCount == 34:
            finalcode = "".join(dataBits)
            print("bin in: %s" % finalcode)
            print("dec in: %d" % int(finalcode, 2))
            print("hex in: " + hex(int(finalcode, 2)))
            intsift = int(finalcode, 2) >> 1
            print("int shift in: %d " % intsift)
            print("bin shift in: " + bin(intsift))
            hexadecimal = hex(intsift)[2:]
            print(hexadecimal)

            bitCount = 0
            dataBits = []
            justRead = 0
        if justRead == 1:
            if bitCount > 34:
                print("is more than 34")
            # Rest of the code just handles the information and prints to a screen.
            # The issue existed before I wrote the rest of the code