'''
Packet sniffer in python using the pcapy python library
 
Project website
http://oss.coresecurity.com/projects/pcapy.html
'''

# See this scapy rssi example
# https://github.com/azz2k/scapy-rssi/blob/master/scapy-rssi.py
 
import socket
from struct import *
import datetime	
import pcapy
import sys
import scapy.all as sca
import scapy_ex
import struct   


import time
import thread
import threading
import signal
import sys
 
def startWifiLoop(interface, targetList, distance):
    
    while True:
        packets = sca.sniff(iface=interface, count = 1)

        for pkt in packets:
            #pkt.show()
            print("Mac 1: ") + str(pkt.addr1)
            print("Mac 2: ") + str(pkt.addr2)
            print("Mac 3: ") + str(pkt.addr3)
            print("Signal Strength: " + str(pkt.dBm_AntSignal))
 
if __name__ == "__main__":
  main(sys.argv)
