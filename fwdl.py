#!/usr/bin/python

import usb.core
import usb.util
import time

vendor = 0x03f0
product = 0x311d
firmware = 'ath3k-1.fw'

dev = usb.core.find(idVendor = vendor, idProduct = product)

if dev is None:
	print('Device not found')
	quit()

print('Device found, waiting for it to be free...')

while True:
	# Have to look again for device in order to get new handle
	dev = usb.core.find(idVendor = vendor, idProduct = product)
	
	try:
		dev.set_configuration()
	except:
		time.sleep(0.1)		
	else:
		print("Device is free, sending firmware...")
		break


with open(firmware, 'r') as f:
	buf = f.read(20)
	assert dev.ctrl_transfer(0x40, 0x01, 0, 0, buf) == len(buf)
	buf = f.read(4096)
	while (buf):
		assert dev.write(2, buf, 100) == len(buf)
		buf = f.read(4096)
	print('Firmware sent, Enjoy :)')
