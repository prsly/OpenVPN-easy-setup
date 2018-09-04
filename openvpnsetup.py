import os
import sys
import subprocess
import getpass

iam = getpass.getuser()
if (iam != "root") :
    print("You must be root to use this script")
    sys.exit(1)

if (os.path.isdir("/dev/net/tun")):
    print("TUN/TAP is enabled")
else:
    print("TUN/TAP is disabled. Contact your VPS provider to enable it")
    sys.exit(2)

ipv4forward = subprocess.call('sysctl net.ipv4.ip_forward | grep 0', shell=True, stdout=subprocess.PIPE)

if (ipv4forward == 0):
    subprocess.call('sysctl -w net.ipv4.ip_forward=1', shell=True, stdout=subprocess.PIPE)
    conf = open('/etc/sysctl.conf', 'a')
    conf.write('net.ipv4.ip_forward = 1')
    conf.close()
else:
    print("IPv4 forwarding is already enabled")    