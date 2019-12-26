# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'devicelist.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DeviceListDialog(object):
    def setupUi(self, DeviceListDialog):
        DeviceListDialog.setObjectName("DeviceListDialog")
        DeviceListDialog.resize(277, 281)
        self.buttonBox_deviceList = QtWidgets.QDialogButtonBox(DeviceListDialog)
        self.buttonBox_deviceList.setGeometry(QtCore.QRect(60, 240, 161, 32))
        self.buttonBox_deviceList.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_deviceList.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_deviceList.setObjectName("buttonBox_deviceList")
        self.tableWidget = QtWidgets.QTableWidget(DeviceListDialog)
        self.tableWidget.setGeometry(QtCore.QRect(25, 21, 221, 191))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)

        self.retranslateUi(DeviceListDialog)
        self.buttonBox_deviceList.rejected.connect(DeviceListDialog.reject)
        self.buttonBox_deviceList.accepted.connect(DeviceListDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(DeviceListDialog)

    def retranslateUi(self, DeviceListDialog):
        _translate = QtCore.QCoreApplication.translate
        DeviceListDialog.setWindowTitle(_translate("DeviceListDialog", "Dialog"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("DeviceListDialog", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("DeviceListDialog", "2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("DeviceListDialog", "3"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("DeviceListDialog", "4"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("DeviceListDialog", "5"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("DeviceListDialog", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("DeviceListDialog", "Model Name"))
