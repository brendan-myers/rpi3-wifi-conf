#!/usr/bin/env python

import os
from bluetooth import *
import subprocess
import time

def wifi_connect(ssid, psk):
    # write wifi config to file
    f = open('wifi.conf', 'w')
    f.write('country=GB\n')
    f.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
    f.write('update_config=1\n')
    f.write('\n')
    f.write('network={\n')
    f.write('    ssid="' + ssid + '"\n')
    f.write('    psk="' + psk + '"\n')
    f.write('}\n')
    f.close()

    cmd = 'mv wifi.conf /etc/wpa_supplicant/wpa_supplicant.conf'
    cmd_result = ""
    cmd_result = os.system(cmd)
    print cmd + " - " + str(cmd_result)


    # restart wifi adapter
    cmd = 'sudo ifdown wlan0'
    cmd_result = os.system(cmd)
    print cmd + " - " + str(cmd_result)

    time.sleep(2)

    cmd = 'sudo ifup wlan0'
    cmd_result = os.system(cmd)
    print cmd + " - " + str(cmd_result)

    time.sleep(10)

    cmd = 'iwconfig wlan0'
    cmd_result = os.system(cmd)
    print cmd + " - " + str(cmd_result)

    cmd = 'ifconfig wlan0'
    cmd_result = os.system(cmd)
    print cmd + " - " + str(cmd_result)

    p = subprocess.Popen(['ifconfig', 'wlan0'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    out, err = p.communicate()

    ip_address = "<Not Set>"

    for l in out.split('\n'):
        if l.strip().startswith("inet addr:"):
            ip_address = l.strip().split(' ')[1].split(':')[1]

    return ip_address


try:
    while True:
        server_sock=BluetoothSocket( RFCOMM )
        server_sock.bind(("",PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        uuid = "815425a5-bfac-47bf-9321-c5ff980b5e11"

        advertise_service( server_sock, "RPi Wifi config",
                           service_id = uuid,
                           service_classes = [ uuid, SERIAL_PORT_CLASS ],
                           profiles = [ SERIAL_PORT_PROFILE ])


        print "Waiting for connection on RFCOMM channel %d" % port

        client_sock, client_info = server_sock.accept()
        print "Accepted connection from ", client_info


        ssid = ""
        psk = ""


        # get ssid
        client_sock.send("waiting-ssid!")
        print "Waiting for SSID..."

        while True:
            data = client_sock.recv(1024)
            ssid = data
            print "ssid received"

            break

        print ssid


        # get psk
        client_sock.send("waiting-psk!")
        print "Waiting for PSK..."

        while True:
            data = client_sock.recv(1024)
            psk = data
            print "psk received"

            break

        print psk

        ip_address=wifi_connect(ssid, psk)

        print "ip address: " + ip_address

        client_sock.send("ip-addres:" + ip_address + "!")
        client_sock.close()
        server_sock.close()

        # finished config
        print 'Finished configuration\n'


except (KeyboardInterrupt, SystemExit):
    print '\nExiting\n'
