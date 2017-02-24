# Watches nearby BT and WIFI 
# buzzes when target within some range

# Written by Chase McCarty, January 2017


from wifi import startWifiLoop
from bt import startBtLoop

def main():
	# make sure these are lower case
	targetWifiMacs = ["44:00:10:3f:2a:b7"]
	targetBTMacs = ["44:00:10:3f:2a:b8", "f4:0f:24:2c:49:f4"]
	targetWifiDistance = -40
	targetBTDistance = -40


	startWifiLoop("mon0", targetWifiMacs, targetWifiDistance)
	#startBtLoop(targetBTMacs, targetBTDistance)

main()
