import os
import sys
import glob


class SCSI:
    def __init__(self):
        SCSI_DEV_PATH = '/sys/bus/scsi/devices'
        dev_paths = [os.path.join(SCSI_DEV_PATH, path) for path in os.listdir(SCSI_DEV_PATH) if path.replace(':', '').isnumeric()]
        for dev_path in dev_paths:
            print(self._name(dev_path), self._dev(dev_path))

    def _name(self, dev_path):
        with open(os.path.join(dev_path, 'model'), 'r')as fp:
            name = fp.read()
        return name

    def _dev(self, dev_path):
        dev = os.listdir(os.path.join(dev_path, 'block'))
        block_path = os.path.join(dev_path, 'block')
        _ = os.path.join(block_path, dev[0])
        blocks = list(glob.iglob(os.path.join(_,  dev[0] + '*')))
        return (dev[0], [os.path.join('/dev', os.path.split(block)[-1]) for block in blocks])
print(SCSI())
