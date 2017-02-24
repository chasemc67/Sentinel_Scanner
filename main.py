# Watches nearby BT and WIFI 
# buzzes when target within some range

# Written by Chase McCarty, January 2017


from wifi import startWifiLoop

def main():
	targetWifiMacs = ["44:00:10:3f:2a:b7"]
	targetBTMacs = ["44:00:10:3F:2A:B8"]
	targetWifiDistance = -40
	targetBTDistance = -40


	startWifiLoop("mon0", targetWifiMacs, targetWifiDistance)


main()
