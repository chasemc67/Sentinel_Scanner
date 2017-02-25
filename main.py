# Watches nearby BT and WIFI 
# buzzes when target within some range

# Written by Chase McCarty, January 2017


from wifi import WifiThread
from bt import BtThread
import threading
import time
import Queue

threads = []

def printBuzzer(wifiQueue, btQueue):

	if not wifiQueue.empty():
		buzzWifi = False
		while(not wifiQueue.empty()):
			wifiTuple = wifiQueue.get()
			#print("seen Wifi " + str(wifiTuple[1]))
			buzzWifi = buzzWifi or wifiTuple[0]
	else:
		buzzWifi = "unknown"

	if not btQueue.empty():
		buzzBt = False
		while(not btQueue.empty()):
			btTuple = btQueue.get()
			#print("seen BT " + str(btTuple[1]))
			buzzBt = buzzBt or btTuple[0]
	else:
		buzzBt = "unknown"
	
	if buzzWifi == "unknown":
		print("Wifi unknown")

	if buzzBt == "unknown":
		print("Bt unknown")

	if buzzWifi == True:
		print("Wifi is on")
	elif: buzzWifi == False:
		print("Wifi is off")

	if buzzBt == True:
		print("Bt is on")
	elif: buzzBt == False:
		print("Bt is off")

	'''
	if buzzWifi == True and buzzBt == True:
		print("Wifi is on, BT is on")
	elif buzzWifi == True and buzzBt == False:
		print("Wifi is on, BT is off")
	elif buzzWifi == False and buzzBt == True:
		print("Wifi is off, BT is on")
	else:
		print("Wifi is off, BT is off")
	'''


def main():
	# make sure these are lower case
	targetWifiMacs = ["44:00:10:3f:2a:b7"]
	targetBTMacs = ["44:00:10:3f:2a:b8", "f4:0f:24:2c:49:f4"]
	targetWifiDistance = -65
	targetBTDistance = -65
	scanTime = 5

	# Queue objects for communicating with threads
	wifiQueue = Queue.Queue()
	btQueue = Queue.Queue()

	threads = [WifiThread("mon0", targetWifiMacs, targetWifiDistance, wifiQueue), BtThread(targetBTMacs, targetBTDistance, btQueue)]

	for thread in threads:
		thread.start()

	while True:
		printBuzzer(wifiQueue, btQueue)
		time.sleep(scanTime)

try:
	main()
except KeyboardInterrupt:
	for thread in threads:
		thread.kill()
