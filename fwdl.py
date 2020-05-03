#!/usr/bin/python

import usb.core
import usb.util
import time

firm = 'ath3k-1.fw'

dev = usb.core.find(idVendor=0x03f0, idProduct=0x311d)

if dev is None:
	print("Device not found")
	quit()

print("Device found, waiting for it to be free...")

while True:
	dev = usb.core.find(idVendor=0x03f0, idProduct=0x311d)
	
	try:
		dev.set_configuration()
	except:
		time.sleep(0.1)		
	else:
		print("Device is free, sending firmware...")
		break


f = open(firm, 'r')
buf = f.read(20)
assert dev.ctrl_transfer(0x40, 0x01, 0, 0, buf) == len(buf)
buf = f.read(4096)
while (buf):
	assert dev.write(2, buf, 100) == len(buf)
#	print len(buf)
	buf = f.read(4096)


