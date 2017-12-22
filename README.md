# rpi3-wifi-conf
A simple Python script to configure wifi over bluetooth for a Raspberry Pi 3

Use [this Android application](https://github.com/brendan-myers/rpi3-wifi-conf-android) to send wifi config details to the Pi.


## Setup

1. Install bluez (Python bluetooth library):

        sudo apt-get install python-bluez


2. Start the bluetooth daemon in compatibility mode, edit `/etc/systemd/system/dbus-org.bluez.service`, and modify the `ExecStart` param:


        ExecStart=/usr/lib/bluetooth/bluetoothd -C


3. Load serial port profile:

        sudo sdptool add SP


4. Restart your Pi:

        sudo reboot


5. Pair your phone with your Raspberry Pi. Turn your phone's bluetooth on. On your Pi:

        bluetoothctl
        power on
        discoverable on
        scan on


  Your phone will appear in the list of available deivces. Take note of the address of your phone.

        trust <PHONE_ADDRESS>
        pair <PHONE_ADDRESS>


  Accept the pin, and exit bluetooth ctl:

        quit



## Running the script

Make script executable:

    chmod +x run.py


To run:

    sudo ./run.py


To run on startup, edit `/etc/rc.local` and add:

    (sleep 10;/path/to/script/./run.py)&
