from PyQt5 import QtWidgets

#UI modules
from .devicelist import Ui_DeviceListDialog

import sys
sys.path.append('../')

#SDK modules
from SDK import device
from SDK import scan
from SDK import scanconfig

class ISC:
    def __init__(self):
        self.device = device.Device()
        self.scan = scan.Scan()
        self.cfg = scanconfig.ScanConfig()

class DevicesUI(QtWidgets.QDialog, Ui_DeviceListDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        print('Devices Dialog init')