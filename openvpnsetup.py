import os
import sys
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