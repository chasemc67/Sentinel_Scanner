import bluetooth

targetMac = "44:00:10:3F:2A:B8"

nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("found %d devices" % len(nearby_devices))

for addr, name in nearby_devices:
	print(" %s - %s"  % (addr, name))
	#print(str(bluetooth.hci_get_route(addr)))

print("Attempting to find mac: " + targetMac)
btName = bluetooth.lookup_name(targetMac)

if btName:
	print("Detected Device: " + btName)
else:
	print("Could not detect device with mac: " + targetMac)

#for A in dir(nearby_devices):
#	print(str(A)+ "\n")

#for f in nearby_devices:
#	print(str(f))

