from PyQt5 import QtWidgets, QtGui
import sys

from Forms import main_ui

class ISC_program:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon('ISC_Logo.ico'))
        ui = main_ui.MainUI()
        ui.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    ISC_program()