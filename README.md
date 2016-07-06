# rpi3-wifi-conf
A simple Python script to configure wifi over bluetooth for a Raspberry Pi 3

Use [this Android application](https://github.com/brendan-myers/rpi3-wifi-conf-android) to send wifi config details to the Rasperry Pi running this script.

Make script executable:

    chmod +x run.py


To run:

    sudo ./run.py


To run on startup, edit `/etc/rc.local` and add:

    (sleep 10;/path/to/script/./run.py)&


