# A module used to sniff for wifi macs within some range.
# See scapy_ex.py for how the packets are parsed
 
import scapy.all as sca
import scapy_ex
 
def startWifiLoop(interface, targetList, distance):
    packets = sca.sniff(iface=interface, count = 10)
    for pkt in packets:
        if pkt.addr2 in targetList:
            if abs(pkt.dBm_AntSignal) <= abs(distance):
                print("[+] " + str(pkt.addr2) + " Seen within range")
            else:
                print("[-] " + str(pkt.addr2) + " Seen but not within range")
