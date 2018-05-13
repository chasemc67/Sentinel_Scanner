### Sentinal Scanner is software built to run on a Raspberry Pi, which alerts users to the presenced of specified people.


Sentinal Scanner watches the airspace for nearby wifi and bluetooth devices.
When a target mac address is seen, and is within some range (determined by signal strength) user will be notified via a buzzer.

For bluetooth, if device is not in discovery mode, user is notified if device is in any communication range


Target macs are hardcoded as lists at the top if main.py for now.

Scan time is hardcoded at 5 second intervals right now

#### Usage:
```
sudo setup.sh
sudo python main.py
```

#### Teardown:
```
sudo teardown.sh
```

#### Installation Requirements:

##### BT:
	```
	sudo apt-get update
	sudo apt-get install python-pip python-dev ipython
	sudo apt-get install bluetooth libbluetooth-dev
	sudo pip install pybluez
	```

##### WiFi:
	```
	sudo apt-get install aircrack-ng
	sudo apt-get install scapy
	```
