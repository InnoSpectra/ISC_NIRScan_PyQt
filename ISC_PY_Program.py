# -*- coding: utf-8 -*-
"""
    The ISC NIRScan GUI SDK Python program supports ISC Pyton SDK through
    PyQt5.
    Copyright (C) 2019  Inno-Spectra Corporation

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
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