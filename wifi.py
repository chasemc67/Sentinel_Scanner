# http://www.binarytides.com/code-a-packet-sniffer-in-python-with-pcapy-extension/

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
 
def main(argv):
    #list all devices
    devices = pcapy.findalldevs()
    print devices
     
    #ask user to enter device name to sniff
    print "Available devices are :"
    for d in devices :
        #print d
        if d.startswith("mon0"):
            dev = d
     
    #dev = raw_input("Enter device name to sniff : ")
     
    print "Sniffing device " + dev
     
    '''
    open device
    # Arguments here are:
    #   device
    #   snaplen (maximum number of bytes to capture _per_packet_)
    #   promiscious mode (1 for true)
    #   timeout (in milliseconds)
    '''

    #cap = pcapy.open_live(dev , 65536 , True , 0)
    packets = sca.sniff(iface=dev, count = 40)

    for pkt in packets:
        pkt.show()
        #print parsePacketSca(pkt)
 
    #start sniffing packets
    #while(1) :
     #   (header, packet) = cap.next()
        #print ('%s: captured %d bytes, truncated to %d bytes' %(datetime.datetime.now(), header.getlen(), header.getcaplen()))
      #  parse_packet(packet)
 
#Convert a string of 6 characters of ethernet address into a dash separated hex string
def eth_addr (a) :
    b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
    return b

def parsePacketSca(pkt):
    pkt.show()
    print "Parsing packet"
    if pkt.haslayer(sca.Dot11):
      print "1"
      if pkt.addr2 is not None:
        print "2"
        # check available Radiotap fields
        field, val = pkt.getfield_and_val("present")
        names = [field.names[i][0] for i in range(len(field.names)) if (1 << i) & val != 0]
        # check if we measured signal strength
        if "dBm_AntSignal" in names:
          print "3"
          # decode radiotap header
          fmt = "<"
          rssipos = 0
          for name in names:
            # some fields consist of more than one value
            if name == "dBm_AntSignal":
              # correct for little endian format sign
              rssipos = len(fmt)-1
            fmt = fmt + self.radiotap_formats[name]
          # unfortunately not all platforms work equally well and on my arm
          # platform notdecoded was padded with a ton of zeros without
          # indicating more fields in pkt.len and/or padding in pkt.pad
          decoded = struct.unpack(fmt, pkt.notdecoded[:struct.calcsize(fmt)])
          return pkt.addr2, decoded[rssipos]
    return None, None
 
#function to parse a packet
def parse_packet(packet) :
     
    #parse ethernet header
    eth_length = 14
     
    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH' , eth_header)
    eth_protocol = socket.ntohs(eth[2])
    print 'Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol)

    if packet.addr2 is not None:
        print("Addr2 is not None")
 
    #Parse IP packets, IP Protocol number = 8
    if eth_protocol == 8 :
        #Parse IP header
        #take first 20 characters for the ip header
        ip_header = packet[eth_length:20+eth_length]
         
        #now unpack them :)
        iph = unpack('!BBHHHBBH4s4s' , ip_header)
 
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
 
        iph_length = ihl * 4
 
        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);
 
        #print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)

 
        #TCP protocol
        if protocol == 6 :
            t = iph_length + eth_length
            tcp_header = packet[t:t+20]
 
            #now unpack them :)
            tcph = unpack('!HHLLBBHHH' , tcp_header)
             
            source_port = tcph[0]
            dest_port = tcph[1]
            sequence = tcph[2]
            acknowledgement = tcph[3]
            doff_reserved = tcph[4]
            tcph_length = doff_reserved >> 4
             
            #print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)

             
            h_size = eth_length + iph_length + tcph_length * 4
            data_size = len(packet) - h_size
             
            #get data from the packet
            data = packet[h_size:]
             
            #print 'Data : ' + data

 
        #ICMP Packets
        elif protocol == 1 :
            u = iph_length + eth_length
            icmph_length = 4
            icmp_header = packet[u:u+4]
 
            #now unpack them :)
            icmph = unpack('!BBH' , icmp_header)
             
            icmp_type = icmph[0]
            code = icmph[1]
            checksum = icmph[2]
             
            #print 'Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum)

             
            h_size = eth_length + iph_length + icmph_length
            data_size = len(packet) - h_size
             
            #get data from the packet
            data = packet[h_size:]
             
            #print 'Data : ' + data

 
        #UDP packets
        elif protocol == 17 :
            u = iph_length + eth_length
            udph_length = 8
            udp_header = packet[u:u+8]
 
            #now unpack them :)
            udph = unpack('!HHHH' , udp_header)
             
            source_port = udph[0]
            dest_port = udph[1]
            length = udph[2]
            checksum = udph[3]
             
            #print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(length) + ' Checksum : ' + str(checksum)

             
            h_size = eth_length + iph_length + udph_length
            data_size = len(packet) - h_size
             
            #get data from the packet
            data = packet[h_size:]
             
            #print 'Data : ' + data

 
        #some other IP packet like IGMP
        else :
            print 'Protocol other than TCP/UDP/ICMP'
             
        print
 
if __name__ == "__main__":
  main(sys.argv)
