# A module used to find nearby bluetooth devices.
# Alerts user if any devices in target list are nearby and within 
# some distance. 

# If a target device is not in discovery mode, range cannot be determined,
# In this case, we still alert the user if we see the device

import bluetooth

from inquiryWithRssi import inquiryWithRssi

def addrFoundWithRssi(addr, results):
	found = False
	for i in results:
		if i[0].lower == addr.lower() and i[1] != -1:
			found = True
	return found


def startBtLoop(targetList, distance):

	while True:
		results = inquiryWithRssi()

		for result in results:
			if result[0].lower() in targetList:
				if abs(result[1]) <= abs(distance):
					print("[+] " + result[0] + " seen within range")
				else:
					print("[-] " + result[0] + " seen but not within range")


		nearby_devices = bluetooth.discover_devices(lookup_names=True)	
		for mac in targetList:
			if not addrFoundWithRssi(mac, results):
				btName = bluetooth.lookup_name(mac)

				if btName:
					print("[*] " + result[0] + " seen at unknown range")
					

