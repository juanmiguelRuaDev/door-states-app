import usb.core
import usb.util

dev = usb.core.find (idVendor=0x72f, idProduct=0x2200)

print (dev)
