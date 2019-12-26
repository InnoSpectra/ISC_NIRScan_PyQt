from PyQt5 import QtWidgets
import sys

from Forms import main_ui

class ISC_program:
    def __init__(self):
        print('In program')
        app = QtWidgets.QApplication(sys.argv)
        ui = main_ui.MainUI()
        ui.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    ISC_program()