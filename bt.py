# A module used to find nearby bluetooth devices.
# Alerts user if any devices in target list are nearby and within 
# some distance. 

# If a target device is not in discovery mode, range cannot be determined,
# In this case, we still alert the user if we see the device

import bluetooth

from inquiryWithRssi import inquiryWithRssi

import threading

class BtThread(threading.Thread):

	def __init__(self, targetList, distance, buzzer):
		super(WifiThread,  self).__init__()
		self.targetList = targetList
		self.distance = distance
		self.buzzer = buzzer
		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			try:
				self.startBtLoop()


	def join(self, timeout=None):
		self.stoprequest.set()
		super(BtThread, self).join(timeout)

	def addrFoundWithRssi(self, addr, results):
		found = False
		for i in results:
			if i[0].lower == addr.lower() and i[1] != -1:
				found = True
		return found


	def startBtLoop(self):

		results = inquiryWithRssi()

		for result in results:
			if result[0].lower() in self.targetList:
				if abs(result[1]) <= abs(self.distance):
					print("[+] BT " + result[0] + " seen within range")
					self.buzzer = True
				else:
					print("[-] BT " + result[0] + " seen but not within range")
					self.buzzer = False


		nearby_devices = bluetooth.discover_devices(lookup_names=True)	
		for mac in self.targetList:
			if not addrFoundWithRssi(mac, results):
				btName = bluetooth.lookup_name(mac)

				if btName:
					print("[*] BT " + str(mac) + " seen at unknown range")
					self.buzzer = True
					

