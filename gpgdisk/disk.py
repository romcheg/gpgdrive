import sys

import faulthandler
import fuse
from gpgdisk import manager


def main():
    faulthandler.enable()

    if len(sys.argv) != 3:
        print('usage: %s <disk> <mountpoint>' % sys.argv[0])
        exit(1)

    op_mgr = manager.DiskManager(sys.argv[1])
    fuse_inst = fuse.FUSE(op_mgr, sys.argv[2], foreground=True)
