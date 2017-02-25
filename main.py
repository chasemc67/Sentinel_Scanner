# Watches nearby BT and WIFI 
# buzzes when target within some range

# Written by Chase McCarty, January 2017


from wifi import WifiThread
from bt import BtThread
import threading
import time
import Queue

threads = []

def printBuzzer(wifiBuzzer, btBuzzer):

	buzzWifi = False
	buzzBt = False

	while(not wifiBuzzer.empty()):
		buzzWifi = buzzWifi or wifiBuzzer.get()

	while(not btBuzzer.empty()):
		buzzBt = buzzBt or btBuzzer.get()

	if buzzWifi == True and buzzBt == True:
		print("Wifi is on, BT is on")
	elif buzzWifi == True and buzzBt == False:
		print("Wifi is on, BT is off")
	elif buzzWifi == False and buzzBt == True:
		print("Wifi is off, BT is on")
	else:
		print("Wifi is off, BT is off")


def main():
	# make sure these are lower case
	targetWifiMacs = ["44:00:10:3f:2a:b7"]
	targetBTMacs = ["44:00:10:3f:2a:b8", "f4:0f:24:2c:49:f4"]
	targetWifiDistance = -65
	targetBTDistance = -65

	wifiBuzzing = Queue.Queue()
	btBuzzing = Queue.Queue()

	threads = [WifiThread("mon0", targetWifiMacs, targetWifiDistance, wifiBuzzing), BtThread(targetBTMacs, targetBTDistance, btBuzzing)]

	for thread in threads:
		thread.start()

	while True:
		printBuzzer(wifiBuzzing, btBuzzing)
		time.sleep(2)

try:
	main()
except KeyboardInterrupt:
	for thread in threads:
		thread.kill()
