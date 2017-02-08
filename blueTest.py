import bluetooth

nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("found %d devices" % len(nearby_devices))

for addr, name in nearby_devices:
	print(" %s - %s"  % (addr, name))
	#print(str(bluetooth.hci_get_route(addr)))

#for A in dir(nearby_devices):
#	print(str(A)+ "\n")

#for f in nearby_devices:
#	print(str(f))

