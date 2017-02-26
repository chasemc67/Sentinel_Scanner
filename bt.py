# A module used to find nearby bluetooth devices.
# Alerts user if any devices in target list are nearby and within 
# some distance. 

# If a target device is not in discovery mode, range cannot be determined,
# In this case, we still alert the user if we see the device

import bluetooth
from inquiryWithRssi import inquiryWithRssi
import threading
import Queue

class BtThread(threading.Thread):

	def __init__(self, targetList, distance, buzzer):
		super(BtThread,  self).__init__()
		self.targetList = targetList
		self.distance = distance
		self.buzzer = buzzer
		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			self.btLoop()


	def join(self, timeout=None):
		self.stoprequest.set()
		super(BtThread, self).join(timeout)

	def addrFoundWithRssi(self, addr, results):
		found = False
		for i in results:
			if i[0].lower == addr.lower() and i[1] != -1:
				found = True
		return found


	def btLoop(self):

		# Check for nearby BT devices in discovery mode
		# and get their RSSIs
		results = inquiryWithRssi()

		for result in results:
			if result[0].lower() in self.targetList
				if abs(result[1]) <= abs(self.distance):
					#print("[+] BT " + result[0] + " seen within range")
					self.buzzer.put((True, result[0]))
				else:
					#print("[-] BT " + result[0] + " seen but not within range")
					self.buzzer.put((False, result[0]))
			else:
				self.buzzer.put((False, result[0]))

		# Force check for nearby targets not in discovery mode
		# Cant get RSSIs
		nearby_devices = bluetooth.discover_devices(lookup_names=True)	
		for mac in self.targetList:
			if not self.addrFoundWithRssi(mac, results):
				btName = bluetooth.lookup_name(mac)

				if btName:
					#print("[*] BT " + str(mac) + " seen at unknown range")
					self.buzzer.put((True, mac))
				else:
					self.buzzer.put((False, "00:00:00:00"))
		


