import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

file1 = open('testimage.jpg','w')

while True:
    str1 = ser.read(24)
    response = str1.decode('ascii')
    if response != '' and len(response) == 24:
        """valueint = int(response.replace('o', '0'))
        valuehex = hex(valueint)
        file1.write(valuehex)"""
        value_hex = response[16:]
        print("all:[%s]- len:[%d] - card:[%s]" % (response, len(response), value_hex))
