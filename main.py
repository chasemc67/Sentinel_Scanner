# Watches nearby BT and WIFI 
# buzzes when target within some range

# Written by Chase McCarty, January 2017

from wifi import WifiThread
from bt import BtThread
import threading
import time
import Queue

# Configure targets and distance here
#######################################
targetWifiMacs = ["44:00:10:3f:2a:b7"] # make sure these are lower case
targetBTMacs = ["44:00:10:3f:2a:b8", "00:1a:7d:da:71:13"] # make sure these are lower case
targetWifiDistance = -65
targetBTDistance = -65
scanTime = 9	# time to sleep between scans (BT scan takes ~10 seconds)
#######################################


threads = []
buzzBt = False
buzzWifi = False

def main():
	# Queue objects for communicating with threads
	wifiQueue = Queue.Queue()
	btQueue = Queue.Queue()

	# Multithreading so we can look for BT and wifi simultaneously
	threads = [WifiThread("mon0", targetWifiMacs, targetWifiDistance, wifiQueue), BtThread(targetBTMacs, targetBTDistance, btQueue)]

	for thread in threads:
		thread.start()

	while True:
		printBuzzer(wifiQueue, btQueue)
		time.sleep(scanTime)

# Print function in instead of buzzer
def printBuzzer(wifiQueue, btQueue):	
	global buzzBt
	global buzzWifi

	if not wifiQueue.empty():
		buzzWifi = False
		while(not wifiQueue.empty()):
			wifiTuple = wifiQueue.get()
			buzzWifi = buzzWifi or wifiTuple[0]

	if not btQueue.empty():
		buzzBt = False
		while(not btQueue.empty()):
			btTuple = btQueue.get()
			buzzBt = buzzBt or btTuple[0]

	print("")

	if buzzWifi == True:
		print("Wifi is on")
	elif buzzWifi == False:
		print("Wifi is off")

	if buzzBt == True:
		print("Bt is on")
	elif buzzBt == False:
		print("Bt is off")

	print("")

# except keyboard interrupt to kill other threads
try:
	main()
except KeyboardInterrupt:
	for thread in threads:
		thread.kill()
