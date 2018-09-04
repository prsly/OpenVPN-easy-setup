# Express setup of OpenVPN server
# for Ubuntu Server 16.x / 17.x
# by xl-tech https://github.com/xl-tech
# fork by prsly https://github.com/prsly
#
# Version 1.0 4.09.2018
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
import getpass
import subprocess
import sys
import shutil


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


def subcall(arg, pipe):
    if pipe == 1:
        return subprocess.call(arg, shell=True, stdout=subprocess.PIPE)
    else:
        return subprocess.call(arg, shell=True)


def subpopen(arg):
    return subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)


print('1 --- Checking superuser permission')
iam = getpass.getuser()
if (iam != 'root'):
    print('You must be root to use this script')
    sys.exit(1)

print('2 --- Checking TUN/TAP')
if (os.path.isdir('/dev/net/tun')):
    print('TUN/TAP is enabled')
else:
    print('TUN/TAP is disabled. Contact your VPS provider to enable it')
    sys.exit(2)

print('3 --- Checking IPv4 Forwarding')
ipv4forward = subcall('sysctl net.ipv4.ip_forward | grep 0', 1)
if (ipv4forward == 0):
    subcall('sysctl -w net.ipv4.ip_forward=1', 1)
    conf = open('/etc/sysctl.conf', 'a')
    conf.write('net.ipv4.ip_forward = 1')
    conf.close()
else:
    print('IPv4 forwarding is already enabled')

print('4 --- Installing applications')
checkUbuntu = subcall('cat /etc/*release | grep ^NAME | grep Ubuntu', 1)
if (checkUbuntu == 0):
    subcall('apt update')
    subcall('apt upgrade')
    subcall('apt install -y openssl openvpn easy-rsa iptables ' +
            'netfilter-persistent iptables-persistent curl')
    subcall('ufw disable')
else:
    print('This script for Ubuntu. If you want install in CentOS check: ' +
          'http://github.com/xl-tech/OpenVPN-easy-setup')
    sys.exit(3)

iip, temp = subpopen('hostname -I').communicate()
iip = iip.decode('utf-8')[0:-2]

eip, temp = subpopen("curl -s checkip.dyndns.org | sed -e 's/.*" +
                     "Current IP Address: //' -e 's/<.*$//'").communicate()
eip = eip.decode('utf-8')[0:-2]

iipv6, temp = subpopen('ip -6 addr|grep inet6|grep fe80|awk -F ' +
                       "'[ \t]+|' '{print $3}'").communicate()
iipv6 = iipv6.decode('utf-8')[0:-1]

print('Select server IP to listen on (only used for IPv4):\n 1) Internal ' +
      'IP - {i} (in case you are behind NAT)\n 2) '.format(i=iip) +
      'External IP - {e}'.format(e=eip))
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

print('Select server PORT to listen on:\n' +
      ' 1) tcp 443 (recommended)' +
      ' 2) udp 1194 (default)' +
      ' 3) Enter manually (proto port)')
choose = int(input())
for case in switch(choose):
    if case(1):
        port = 'tcp 443'
    if case(2):
        port = 'udp 1194'
    if case(3):
        print('Enter proto and port (like tcp 80 or udp 53): ')
        port = input().lowercase()
    if case():
        print('Invalid option')
portl, portn = port.rsplit(' ')
portl6 = portl + '6'

print('Select server cipher:\n' +
      ' 1) AES-256-GCM (default for OpenVPN 2.4.x, not supported by ' +
      'Ubuntu Server 16.x)\n 2) AES-256-CBC\n 3) AES-128-CBC (default for' +
      ' OpenVPN 2.3.x\n 4) BF-CBC (insecure)')
choose = int(input())
for case in switch(choose):
    if case(1):
        cipher = 'AES-256-GCM'
    if case(2):
        cipher = 'AES-256-CBC'
    if case(3):
        cipher = 'AES-128-CBC'
    if case(4):
        cipher = 'BF-CBC'
    if case():
        print('Invalid option')

print('Enable IPv6? (ensure that your machine have IPv6 support):\n' +
      ' 1) Yes\n 2) No')
choose = int(input())
for case in switch(choose):
    if case(1):
        ipv6e = 1
    if case(2):
        ipv6e = 0
    if case():
        print('Invalid option')

print('Check your selection\n' +
      'Server will listen on {i}\n'.format(i=ip) +
      'Server will listen on {i}\n'.format(i=port) +
      'Server will use {i} cipher\n'.format(i=cipher) +
      'IPv6 - {i} (1 is enabled, 0 is disabled)\n'.format(i=ipv6e))
input('Press Enter to continue...\n')

os.mkdir('/etc/openvpn/easy-rsa/keys')
os.mkdir('/etc/openvpn/logs')
os.mkdir('/etc/openvpn/bundles')
os.mkdir('/etc/openvpn/ccd')
indextxt = os.open('/etc/openvpn/easy-rsa/keys/index.txt', 'a').close()
serial = os.open('/etc/openvpn/easy-rsa/keys/serial',
                 'w').write('00').close()
shutil.copy('/usr/share/easy-rsa/*', '/etc/openvpn/easy-rsa')
