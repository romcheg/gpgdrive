import sys

import llfuse

from gpgdisk import manager


def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: %s <mountpoint>' % sys.argv[0])

    mountpoint = sys.argv[1]
    operations = manager.MountManager()

    llfuse.init(operations, mountpoint, ['fsname=tmpfs', "nonempty" ])

    try:
        llfuse.main(single=True)
    except:
        llfuse.close(unmount=False)
        raise

    llfuse.close()
