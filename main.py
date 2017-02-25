# Watches nearby BT and WIFI 
# buzzes when target within some range

# Written by Chase McCarty, January 2017


from wifi import WifiThread
from bt import BtThread

import threading

def printBuzzer(wifiBuzzer, btBuzzer):
	if wifiBuzzer and btBuzzer:
		print("Wifi is on, BT is on")
	elif wifiBuzzer and not btBuzzer:
		print("Wifi is on, BT is off")
	elif not wifiBuzzer and btBuzzer:
		print("Wifi is off, BT is on")
	else:
		print("Wifi is off, BT is off")

def main():
	# make sure these are lower case
	targetWifiMacs = ["44:00:10:3f:2a:b7"]
	targetBTMacs = ["44:00:10:3f:2a:b8", "f4:0f:24:2c:49:f4"]
	targetWifiDistance = -65
	targetBTDistance = -65

	wifiBuzzing = False
	btBuzzing = True

	threads = [WifiThread("mon0", targetWifiMacs, targetWifiDistance, wifiBuzzing), BtThread(targetBTMacs, targetBTDistance, btBuzzing)]

	for thread in threads:
		thread.start()

	while True:
		printBuzzer(wifiBuzzing, btBuzzing)

main()
