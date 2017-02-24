Cmput 497 Assignment 2

Watches the airspace for nearby wifi and bluetooth devices.
When a target mac address is seen, and is within some range (determined by signal strength) user will be notified.

For bluetooth, if device is not in discovery mode, user is notified if device is in any communication range


Target macs are hardcoded as lists at the top if main.py for now.

usage:

$ sudo setup.sh
$ sudo main.py

after finished run:

$ sudo teardown.sh