#!/usr/bin/python
#
# Express setup of OpenVPN server
# for Ubuntu Server 16.x / 17.x
# by xl-tech https://github.com/xl-tech
# fork by prsly https://github.com/prsly
#
# Version 0.1.1 16.06.2018
#
# Use only on fresh installed machine! It can rewrite your firewall rules
# or your current OpenVPN config (if you have it before).
#
# Script is licensed under the GNU General Public License v3.0
#
# Usage: just run openvpnsetup.py :)
#
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import getpass


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match
        raise StopIteration

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        return False

print("1 --- Checking superuser permission")
iam = getpass.getuser()
if (iam != "root"):
    print("You must be root to use this script")
    sys.exit(1)

print("2 --- Checking TUN/TAP")
if (os.path.isdir("/dev/net/tun")):
    print("TUN/TAP is enabled")
else:
    print("TUN/TAP is disabled. Contact your VPS provider to enable it")
    sys.exit(2)

print("3 --- Checking IPv4 Forwarding")
ipv4forward = subprocess.call('sysctl net.ipv4.ip_forward | grep 0',
                              shell=True, stdout=subprocess.PIPE)
if (ipv4forward == 0):
    subprocess.call('sysctl -w net.ipv4.ip_forward=1',
                    shell=True, stdout=subprocess.PIPE)
    conf = open('/etc/sysctl.conf', 'a')
    conf.write('net.ipv4.ip_forward = 1')
    conf.close()
else:
    print("IPv4 forwarding is already enabled")

print("4 --- Installing applications")
checkUbuntu = subprocess.call('cat /etc/*release | grep ^NAME | grep Ubuntu',
                              shell=True, stdout=subprocess.PIPE)
if (checkUbuntu == 0):
    subprocess.call('apt update', shell=True)
    subprocess.call('apt upgrade', shell=True)
    subprocess.call('apt install -y openssl openvpn easy-rsa iptables ' +
                    'netfilter-persistent iptables-persistent curl',
                    shell=True)
    subprocess.call('ufw disable', shell=True)
else:
    print("This script for Ubuntu. If you want install in CentOS check: " +
          "http://github.com/xl-tech/OpenVPN-easy-setup")
    sys.exit(3)

iip, temp = subprocess.Popen('hostname -I', shell=True,
                             stdout=subprocess.PIPE).communicate()
iip = iip.decode('utf-8')[0:-2]

eip, temp = subprocess.Popen("curl -s checkip.dyndns.org | sed -e 's/.*" +
                             "Current IP Address: //' -e 's/<.*$//'",
                             shell=True, stdout=subprocess.PIPE).communicate()
eip = eip.decode('utf-8')[0:-2]

iipv6, temp = subprocess.Popen("ip -6 addr|grep inet6|grep fe80|awk -F " +
                               "'[ \t]+|' '{print $3}'",
                               shell=True,
                               stdout=subprocess.PIPE).communicate()
iipv6 = iipv6.decode('utf-8')[0:-1]

print(f"Select server IP to listen on (only used for IPv4):\n 1) Internal " +
      f"IP - {iip} (in case you are behind NAT)\n 2) External IP - {eip}")
choose = int(input())
for case in switch(choose):
    if case(1):
        ip = iip
        break
    if case(2):
        ip = eip
        break
    if case():
        print('Invalid option')

print("Select server PORT to listen on:\n" +
      " 1) tcp 443 (recommended)" +
      " 2) udp 1194 (default)"
      " 3) Enter manually (proto (lowercase!) port)")
choose = int(input())
for case in switch(choose):
    if case(1):
        port = "tcp 443"
    if case(2):
        port = "udp 1194"
    if case(3):
        print("Enter proto and port (like tcp 80 or udp 53): ")
        port = input()
    if case():
        print('Invalid option')
portl, portn = port.rsplit(" ")
portl6 = portl + "6"
