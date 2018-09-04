
import getpass

iam = getpass.getuser()
if (iam != "root") :
    print("You must be root to use this script")
    exit