#http://stackoverflow.com/questions/27364581/obtain-bluetooth-signal-strength-on-raspberry-pi-of-bt-device-without-pairing


import bluetooth
import bluetooth._bluetooth as bluez
import struct, socket, sys, select
def hci_enable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x01)

#Discover name and RSS of enabled BLE devices
class MyDiscoverer(bluetooth.DeviceDiscoverer):

    def pre_inquiry(self):
        self.done = False

    def device_discovered(self, address, device_class, rssi, name):
        discovery_logger.info("Discovered %s" % (address, ))
        if name == "iphone":
            #Use the RSS for your detection / localization system

    def inquiry_complete(self):
        self.done = True

#Performs inquiry for name request
def async_inquiry():
    d = MyDiscoverer()
    while True:
        d.find_devices(lookup_names = True)
        readfiles = [ d, ]
        while True:
            rfds = select.select( readfiles, [], [] )[0]
            if d in rfds:
                d.process_event()
            if d.done:
                break
        time.sleep(DISCOVERY_INTERVAL)

#Parse received advertising packets
def parse_events(sock):
# save current filter
old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

flt = bluez.hci_filter_new()
bluez.hci_filter_all_events(flt)
bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )
while True:
    pkt = sock.recv(255)
    ptype, event, plen = struct.unpack("BBB", pkt[:3])
    if event == LE_META_EVENT:
        subevent, = struct.unpack("B", pkt[3])
        pkt = pkt[4:]
        if subevent == EVT_LE_CONN_COMPLETE:
            le_handle_connection_complete(pkt)
        elif subevent == EVT_LE_ADVERTISING_REPORT:
            #Check if the advertisement is the one we are searching for
            if getASCII(pkt[start:end]) == "44:00:10:3F:2A:B8"
                report_pkt_offset = 0
                report_data_length, = struct.unpack("B", pkt[report_pkt_offset + 9])
                # each report is 2 (event type, bdaddr type) + 6 (the address)
                #    + 1 (data length field) + report_data length + 1 (rssi)
                report_pkt_offset = report_pkt_offset +  10 + report_data_length + 1
                rssi, = struct.unpack("b", pkt[report_pkt_offset -1])
                #Now you have the RSS indicator, use it for monitoring / localization

sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
except:
    print "error accessing bluetooth device..."
    sys.exit(1)

p = threading.Thread(group=None, target=parse_events, name='parsing', args=(sock, ))
d = threading.Thread(group=None, target=async_inquiry, name='async_inquiry', args=())
try:
    p.start()
except:
    print "Error: unable to start parsing thread"

try:
    d.start()
except:
    print "Error: unable to start asynchronous discovery thread"