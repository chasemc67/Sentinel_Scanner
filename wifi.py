# A module used to sniff for wifi macs within some range.
# See scapy_ex.py for how the packets are parsed
 
import scapy.all as sca
import scapy_ex
import threading

class WifiThread(threading.Thread)

	def __init__(self, interface, targetList, distance, buzzer):
		super(WifiThread,  self).__init__()
		self.interface = interface
		self.targetList = targetList
		self.distance = distance
		self.buzzer = buzzer
		self.stoprequest = threading.Event()
	 
	def startWifiLoop(self):
	    packets = sca.sniff(iface=self.interface, count = 40)
	    for pkt in packets:
	        if pkt.addr2 in self.targetList:
	            if abs(pkt.dBm_AntSignal) <= abs(self.distance):
	                print("[+] Wifi " + str(pkt.addr2) + " Seen within range")
	                self.buzzer = True
	            else:
	                print("[-] Wifi " + str(pkt.addr2) + " Seen but not within range")
	                self.buzzer = False


	def run(self):
		while not self.stoprequest.isSet():
			try:
				self.startWifiLoop()

	def join(self, timeout=None):
		self.stoprequest.set()
		super(WifiThread, self).join(timeout)