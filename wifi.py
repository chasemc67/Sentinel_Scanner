# A module used to sniff for wifi macs within some range.
# See scapy_ex.py for how the packets are parsed
 
#import socket
#from struct import *
#import datetime	
#import pcapy
#import sys
import scapy.all as sca
import scapy_ex
#import struct   


#import time
#import thread
#import threading
#import signal
#import sys
 
def startWifiLoop(interface, targetList, distance):
    
    while True:
        packets = sca.sniff(iface=interface, count = 1)
        for pkt in packets:
            if pkt.addr2 in targetList:
                if abs(pkt.dBm_AntSignal) <= abs(distance):
                    print("[+] " + str(pkt.addr2) + "Seen within range")
                else:
                    print("[-] " + str(pkt.addr2) + "Seen but not within range")
 
if __name__ == "__main__":
  main(sys.argv)
