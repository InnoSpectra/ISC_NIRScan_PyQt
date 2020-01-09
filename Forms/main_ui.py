# -*- coding: utf-8 -*-
"""
    This file is part of ISC NIRScan GUI SDK Python.

    ISC NIRScan GUI SDK Python is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    ISC NIRScan GUI SDK Python is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from PyQt5 import QtWidgets, QtChart, QtCore, QtGui
import time
import datetime

#UI modules
from .mainwindow import Ui_MainWindow
from .config_ui import ConfigUI
# from .devices_ui import DevicesUI

import sys
sys.path.append('../')
import os

#SDK modules
from SDK import device
from SDK import scan
from SDK import scanconfig

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

class EventMessageBox(QtWidgets.QMessageBox):
    def __init__(self, timeout=3, parent=None, msg="", event=None, param=None):
        super(EventMessageBox, self).__init__(parent)
        self.setWindowTitle("Processing...")
        self.msg = msg

        self.time_to_wait = 5
        self.input_time = timeout
        self.setText(self.msg + ": Please wait about {0} seconds".format(timeout + 5))
        self.setStandardButtons(QtWidgets.QMessageBox.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()
        self.event = None
        self.param = None
        if event is not None:
            self.event = event
        if param is not None:
            self.param = param

    def changeContent(self):
        ret = -1
        if self.time_to_wait == 5:
            if self.event is not None:
                if self.param is not None:
                    print(str(self.event), self.param)
                    ret = self.event(self.param)
                else:
                    print(str(self.event), self.param)
                    ret = self.event()
                if ret < 0:
                    print("Process Failed!")
                    self.setResult(-1)
                self.setResult(0)

        self.setText(self.msg + " ( {0} seconds left)".format(self.time_to_wait))
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()


class MainUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ref_selection = 0
        self.lamp_control = 0
        self.PGA_gain = 64
        self.actived = 0
        self.busy = False

        self.device = device.Device()
        self.scan = scan.Scan()
        self.cfglist = scanconfig.ScanConfig()

        self.setupUi(self)
        self.init_ui()
        self.connectionTimer = QtCore.QTimer()
        self.connectionTimer.setInterval(2000)
        self.connectionTimer.timeout.connect(self._timeout)
        self.connectionTimer.start()

    def init_ui(self):
        self.setWindowTitle("ISC NIRScan GUI SDK Python v1.0.0")

        self.pushButton_edit_scan_config_2.clicked.connect(self.puchButton_edit_scan_config_onClick)
        self.comboBox_scanID.currentIndexChanged.connect(self.comboBox_scanID_indexChange)
        self.radioButton_ref_factory.clicked.connect(self.radioButton_ref_factory_onClick)
        self.radioButton_ref_prev.clicked.connect(self.radioButton_ref_prev_onClick)
        self.radioButton_ref_new.clicked.connect(self.radioButton_ref_new_onClick)
        self.radioButton_always_on.clicked.connect(self.radioButton_always_on_onClick)
        self.radioButton_always_off.clicked.connect(self.radioButton_always_off_onClick)
        self.radioButton_Lamp_Stable_Time.clicked.connect(self.radioButton_Lamp_Stable_Time_onClick)
        self.comboBox_pga_gain.currentIndexChanged.connect(self.comboBox_pga_gain_indexChange)
        self.radioButton_Intensity.clicked.connect(self.radioButton_Intensity_onClick)
        self.radioButton_Absorbance.clicked.connect(self.radioButton_Absorbance_onClick)
        self.radioButton_Reflectance.clicked.connect(self.radioButton_Reflectance_onClick)
        self.radioButton_Reference.clicked.connect(self.radioButton_Reference_onClick)
        self.pushButton_ResetErr.clicked.connect(self.pushButton_ResetErr_onClick)

        self.pushButton_GetModelName_utl.clicked.connect(self.pushButton_GetModelName_utl_onClick)
        self.pushButton_SetModelName_utl.clicked.connect(self.pushButton_SetModelName_utl_onClick)
        self.pushButton_GetSerNumber_utl.clicked.connect(self.pushButton_GetSerNumber_utl_onClick)
        self.pushButton_SetSerNumber_utl.clicked.connect(self.pushButton_SetSerNumber_utl_onClick)
        self.pushButton_GetDateTime.clicked.connect(self.pushButton_GetDateTime_onClick)
        self.pushButton_SyncDateTime.clicked.connect(self.pushButton_SyncDateTime_onClick)
        self.pushButton_GetLampUsage.clicked.connect(self.pushButton_GetLampUsage_onClick)
        self.pushButton_readSensors.clicked.connect(self.pushButton_readSensors_onClick)
        self.pushButton_eeprom_read.clicked.connect(self.pushButton_eeprom_read_onClick)
        self.pushButton_ResetSys.clicked.connect(self.pushButton_ResetSys_onClick)
        self.pushButton_BackUpRef.clicked.connect(self.pushButton_BackUpRef_onClick)
        self.pushButton_ReplaceRef.clicked.connect(self.pushButton_ReplaceRef_onClick)
        self.pushButton_ResotreRef.clicked.connect(self.pushButton_ResotreRef_onClick)
        self.pushButton_set_ActivationKey.clicked.connect(self.pushButton_set_ActivationKey_onClick)
        self.pushButton_clear_ActivactionKey.clicked.connect(self.pushButton_clear_ActivactionKey_onClick)
        self.checkBox_eeprom_writeEN.clicked.connect(self.checkBox_eeprom_writeEN_onClick)
        self.pushButton_eeprom_write.clicked.connect(self.pushButton_eeprom_write_onClick)
        self.pushButton_eeprom_write_generic.clicked.connect(self.pushButton_eeprom_write_generic_onClick)
        self.pushButton_eeprom_restore_default.clicked.connect(self.pushButton_eeprom_restore_default_onClick)
        self.pushButton_tiva_fw_browse.clicked.connect(self.pushButton_tiva_fw_browse_onClick)
        self.pushButton_dlpc_fw_browse.clicked.connect(self.pushButton_dlpc_fw_browse_onClick)
        self.pushButton_tiva_fw_usb_update.clicked.connect(self.pushButton_tiva_fw_usb_update_onClick)
        self.pushButton_dlpc_fw_update.clicked.connect(self.pushButton_dlpc_fw_update_onClick)
        # self.pushButton_deviceList.clicked.connect(self.pushButton_deviceList_onClick)
        self.pushButton_scan.clicked.connect(self.pushButton_scan_onClick)

        #Initialize
        self._chartView()
        self.checkBox_GlitchFilter.setVisible(False)
        self.checkBox_SaveBlackLevel.setVisible(False)
        self.ckb_saveRawADC.setVisible(False)
        self.device.Init()
        self.device.Open()
        time.sleep(2)
        self.SetUiInfo()

        createFolder("InnoSpectra")
        createFolder("InnoSpectra/Reference Data")

    #Scan Page Slots
    def puchButton_edit_scan_config_onClick(self):
        configDialog = ConfigUI(self.device, self.cfglist)
        result = configDialog.exec_()
        if result:
            self._populate_cfglist_comboBox()
        del configDialog

    def radioButton_ref_factory_onClick(self, checked):
        if checked:
            self.ref_selection = 0

    def radioButton_ref_prev_onClick(self, checked):
        if checked:
            self.ref_selection = 1

    def radioButton_ref_new_onClick(self, checked):
        if checked:
            self.ref_selection = 2

    def radioButton_always_on_onClick(self, checked):
        if checked:
            ret = self.scan.SetLamp(1)
            if ret < 0:
                self.ErrorMsg("Fail to set lamp")
            self.lamp_control = 1

    def radioButton_always_off_onClick(self, checked):
        if checked:
            ret = self.scan.SetLamp(2)
            if ret < 0:
                self.ErrorMsg("Fail to set lamp")
            self.lamp_control = 1

    def radioButton_Lamp_Stable_Time_onClick(self, checked):
        if checked:
            ret = self.scan.SetLamp(0)
            if ret < 0:
                self.ErrorMsg("Fail to set lamp")
            self.lamp_control = 0

    def radioButton_Intensity_onClick(self, checked):
        if checked:
            self._clear_plot()
            self._plot()

    def radioButton_Absorbance_onClick(self, checked):
        if checked:
            self._clear_plot()
            self._plot()

    def radioButton_Reflectance_onClick(self, checked):
        if checked:
            self._clear_plot()
            self._plot()
    def radioButton_Reference_onClick(self, checked):
        if checked:
            self._clear_plot()
            self._plot()

    def comboBox_pga_gain_indexChange(self, index):
        PGA_gain = self.comboBox_pga_gain.currentText()
        if len(PGA_gain) < 3:
            self.PGA_gain = int(PGA_gain)
            ret = self.scan.SetFixedPGAGain(True, self.PGA_gain)
            if ret < 0:
                self.ErrorMsg("Connot set PGA gain")
                return

    def comboBox_scanID_indexChange(self, index):
        if index < 0:
            print("Invalid index")
            return
        config = self.cfglist.TargetConfig[index]
        ret = self.cfglist.SetScanConfig(config)
        if ret > 0:
            est_time = self.scan.GetEstimatedScanTime()
            self.label_scan_time_val.setText(str(est_time))

    # def pushButton_deviceList_onClick(self):
    #     deviceDialog = DevicesUI()
    #     result = deviceDialog.exec_()
    #     print('Exit Dialog')
    #     del deviceDialog

    def pushButton_scan_onClick(self):
        self._clear_plot()
        if self.device.IsConnected() == 0:
            self.ErrorMsg("Device not connected")
            return
        if self.actived == 1:
            if self.lamp_control == 0:
                delay = int(self.lineEdit_lamp_stable_time.text())
                ret = self.scan.SetLampDelay(delay)
                if ret < 0:
                    self.ErrorMsg("Cannot set lamp delay time")
                    return
        repeat = self.spinBox_numRepeat.value()
        repeat = int(repeat)
        ret = self.scan.SetScanNumRepeats(repeat)
        if ret < 0:
            return

        # This may be changed based on different Tiva version
        ret = self.scan.SetFixedPGAGain(False, 1)
        if ret != 0:
            self.ErrorMsg("Failed to set PGA gain")

        est_time = int(float(self.label_scan_time_val.text()))
        messagebox = EventMessageBox(est_time, self, "Scan", self.scan.PerformScan, self.ref_selection)
        ret = messagebox.exec_()
        if ret < 0:
            self.ErrorMsg("Scan Failed!")
            return
        if not self.ref_selection == 2:
            ret = self.scan.GetScanConfig()
            if ret < 0:
                self.ErrorMsg("Cannot get Scan Config")
                return
            config = self.scan.scanConfig
            ret = self.device.GetDateTime()
            if ret == 0:
                dateTime = self.device.DevDateTime
                dateTimeStr = str(dateTime['Year']+2000) + str(dateTime['Month']) + str(dateTime['Day']) + "_"
                dateTimeStr = dateTimeStr + str(dateTime['Hour']) + str(dateTime['Minute']) \
                                                                                   + str(dateTime['Second'])
            fileName = "InnoSpectra/" + config[2] + "_" + dateTimeStr + ".dat"
            ret = self.scan.SaveScanResultToBinFile(fileName)
            if ret >= 0:
                self.scan.GetScanResult()
                self._plot()

    def pushButton_ResetErr_onClick(self):
        ret = self.device.ResetErrorStatus()
        time.sleep(1)
        if ret < 0:
            self.ErrorMsg("Failed to reset error message")
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setText("Error Status Reset")
            msgBox.exec_()

    #Utility Page Slots
    def pushButton_GetModelName_utl_onClick(self):
        self.lineEdit_ModelName_utl.setText(self.device.DevInfo['ModelName'])

    def pushButton_SetModelName_utl_onClick(self):
        modelName = self.lineEdit_ModelName_utl.text()
        self.device.SetModelName(modelName)

    def pushButton_GetSerNumber_utl_onClick(self):
        self.lineEdit_SerNumber_utl.setText(self.device.serialNumber)

    def pushButton_SetSerNumber_utl_onClick(self):
        serialNumber = self.lineEdit_SerNumber_utl.text()
        self.device.SetSerialNumber(serialNumber)

    def pushButton_GetDateTime_onClick(self):

        ret = self.device.GetDateTime()
        if ret == 0:
            dateTime = self.device.DevDateTime
            dateTimeStr = str(dateTime['Year']+2000) + "/" + str(dateTime['Month']) + "/" + str(dateTime['Day'])
            dateTimeStr = dateTimeStr + " " + str(dateTime['Hour']) + ":" +str(dateTime['Minute']) + \
                                                                               ":" + str(dateTime['Second'])
        self.lineEdit_DateTime_utl.setText(dateTimeStr)

    def pushButton_SyncDateTime_onClick(self):
        current = str(datetime.datetime.now())
        year = current[0:4]
        month = current[5:7]
        date = current[8:10]
        hour = current[11:13]
        minute = current[14:16]
        second = current[17:19]
        print(year, month, date, hour, minute, second)
        ret = self.device.SetDateTime(int(year),int(month),int(date),int(hour),int(minute),int(second))
        if ret == 0:
            current = current.replace('-', '/')
            self.lineEdit_DateTime_utl.setText(current[:19])

    def pushButton_GetLampUsage_onClick(self):
        if self.actived:
            ret = self.device.ReadLampUsage()
        if ret == 0:
            self.lineEdit_LampUsage_utl.setText(str(self.device.lampUsage))
            self.label_device_LampUsage.setText(str(self.device.lampUsage))

    def pushButton_eeprom_read_onClick(self):
        ret = self.device.GetCalibStruct()
        if ret == 0:
            self.lineEdit_pix2wave0.setText(str(self.device.PixelToWavelengthCoeffs[0]))
            self.lineEdit_pix2wave1.setText(str(self.device.PixelToWavelengthCoeffs[1]))
            self.lineEdit_pix2wave2.setText(str(self.device.PixelToWavelengthCoeffs[2]))
            self.lineEdit_shiftVect0.setText(str(self.device.ShiftVectorCoeffs[0]))
            self.lineEdit_shiftVect1.setText(str(self.device.ShiftVectorCoeffs[1]))
            self.lineEdit_shiftVect2.setText(str(self.device.ShiftVectorCoeffs[2]))
        else:
            self.lineEdit_pix2wave0.setText(str(-1))
            self.lineEdit_pix2wave1.setText(str(-1))
            self.lineEdit_pix2wave2.setText(str(-1))
            self.lineEdit_shiftVect0.setText(str(-1))
            self.lineEdit_shiftVect1.setText(str(-1))
            self.lineEdit_shiftVect2.setText(str(-1))

    def checkBox_eeprom_writeEN_onClick(self, checked):
        if checked:
            self.pushButton_eeprom_write_generic.setEnabled(True)
            self.pushButton_eeprom_restore_default.setEnabled(True)
            self.pushButton_eeprom_write.setEnabled(True)
        else:
            self.pushButton_eeprom_write_generic.setEnabled(False)
            self.pushButton_eeprom_restore_default.setEnabled(False)
            self.pushButton_eeprom_write.setEnabled(False)

    def pushButton_eeprom_write_onClick(self):
        P2W = []
        P2W.append(float(self.lineEdit_pix2wave0.text()))
        P2W.append(float(self.lineEdit_pix2wave1.text()))
        P2W.append(float(self.lineEdit_pix2wave2.text()))
        shiftVector = []
        shiftVector.append(float(self.lineEdit_shiftVect0.text()))
        shiftVector.append(float(self.lineEdit_shiftVect1.text()))
        shiftVector.append(float(self.lineEdit_shiftVect2.text()))
        ret = self.device.SendCalibStruct(P2W, shiftVector)
        if ret < 0:
            print("Fail!")

    def pushButton_eeprom_write_generic_onClick(self):
        ret = self.device.SetGenericCalibStruct()
        if ret < 0:
            print("Fail")

    def pushButton_eeprom_restore_default_onClick(self):
        ret = self.device.RestoreDefaultCalibStruct()
        if ret < 0:
            print("Fail")

    def pushButton_ResetSys_onClick(self):
        self.device.ResetTiva()
        self.device.Exit()
        self.device.Init()

        messagebox = EventMessageBox(5, self, "Reset", self.device.Open)
        ret = messagebox.exec_()

        if ret == 0:
            ret = self.device.IsConnected()
            if ret == 1:
                self.SetUiInfo()
                print("Reset success")
        else:
            self.ErrorMsg("Failed to reset system")

    def pushButton_BackUpRef_onClick(self):
        ret = self.device.BackupFactoryReference(self.device.serialNumber)
        if ret < 0:
            self.ErrorMsg("Fail!")

    def pushButton_ReplaceRef_onClick(self):
        ret = self.cfglist.SetScanConfig(self.cfglist.RefConfig)
        messagebox = EventMessageBox(2, self, "Set Calibration Conifg")
        messagebox.exec_()
        if ret < 0:
            self.ErrorMsg("Fail to set config")
            return

        messagebox = EventMessageBox(5, self, "Scan Calibration Sample", self.scan.PerformScan, 2)
        ret = messagebox.exec_()
        if ret < 0:
            self.ErrorMsg("Scan Failed!")
            return
        ret = self.scan.SaveReferenceScan()
        if ret < 0:
            self.ErrorMsg("Fail to Save New Reference")

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText("Save New Reference Success!")
        msgBox.exec_()

    def pushButton_ResotreRef_onClick(self):
        ret = self.device.RestoreFactoryReference(self.device.serialNumber)
        if ret < 0:
            self.ErrorMsg("Fail!")

    def pushButton_tiva_fw_browse_onClick(self):
        opened_file, file_filter = QtWidgets.QFileDialog.getOpenFileNames( None, \
                                                          'Select bin file to update Tiva:', \
                                                          'C:\\', \
                                                          '*.bin')
        if opened_file != []:
            tiva_file = opened_file[0]
            self.lineEdit_tiva_fw_filename.setText(tiva_file)
            if tiva_file != "":
                self.pushButton_tiva_fw_usb_update.setEnabled(True)

    def pushButton_tiva_fw_usb_update_onClick(self):
        messagebox = EventMessageBox(2, self, "Tiva Update Phase 1", self.device.Tiva_SetTivaToBootloader)
        ret = messagebox.exec_()
        if ret >= 0:
            filePath = self.lineEdit_tiva_fw_filename.text()
            messagebox = EventMessageBox(10, self, "Tiva Update Phase 2", self.device.Tiva_FWUpdate, filePath)
            ret = messagebox.exec_()
            print(ret)
            self.device.Close()
            self.device.Init()
            self.device.Open()
            time.sleep(2)
            self.SetUiInfo()

    def pushButton_dlpc_fw_browse_onClick(self):
        opened_file, file_filter = QtWidgets.QFileDialog.getOpenFileNames( None, \
                                                          'Select img file to update DLPC:', \
                                                          'C:\\', \
                                                          '*.img')
        if opened_file != []:
            tiva_file = opened_file[0]
            self.lineEdit_dlpc_fw_filename.setText(tiva_file)
            if tiva_file != "":
                self.pushButton_dlpc_fw_update.setEnabled(True)

    def pushButton_dlpc_fw_update_onClick(self):
        imgByteBuff = b''
        count = 0
        filepath = self.lineEdit_dlpc_fw_filename.text()

        print(filepath)
        with open(filepath, 'rb') as file:
            while True:
                inbyte = file.read(1)
                if inbyte == b'' or inbyte == '':
                    break
                if count > 200000:
                    break
                imgByteBuff += inbyte
                count += 1
        self.device.DLPC_CheckImageSignature(imgByteBuff)
        self.device.DLPC_SetImageSize(count)
        expectedchecksum = 0
        for i in range(0, count):
            expectedchecksum += imgByteBuff[i]

        byteToSend = count
        bytesSent = 0

        while (byteToSend > 0):
            bytesSent = self.device.DLPC_Update_WriteDate(imgByteBuff[count - byteToSend:count], byteToSend)
            if bytesSent < 0:
                break
            byteToSend -= bytesSent
        messagebox = EventMessageBox(6, self, "DLPC Update ")
        messagebox.exec_()
        self.pushButton_ResetSys_onClick()

    def pushButton_set_ActivationKey_onClick(self):
        keyStr = self.lineEdit_key_number.text()
        ret = self.device.SetActivationKey(keyStr)
        if ret == 0:
            print("Success", self.device.GetActivationResult())
            self._activation_enable()
        else:
            self.ErrorMsg("Failed to set Activation Key")

    def pushButton_clear_ActivactionKey_onClick(self):
        ret = self.device.ClearActivationKey()
        if ret == 0:
            print("Success", self.device.GetActivationResult())
            self._activation_enable()
        else:
            self.ErrorMsg("Failed to Clear Activation Key")

    def pushButton_readSensors_onClick(self):
        self.device.ReadSensorsData()
        self.label_batt_status.setText(self.device.DevSensors['BattStatus'])
        if self.device.DevSensors['BattCapicity'] < 0:
            self.label_batt_volt.setText("Read Failed!")
        else:
            self.label_batt_volt.setText(str(self.device.DevSensors['BattCapicity']))
        if self.device.DevSensors['Humidity'] < 0:
            self.label_hum.setText("Read Failed!")
        else:
            self.label_hum.setText(str(self.device.DevSensors['Humidity']))
        if self.device.DevSensors['HDCTemp'] < 0:
            self.label_hdc_temp.setText("Read Failed!")
        else:
            self.label_hdc_temp.setText(str(self.device.DevSensors['HDCTemp']))
        if self.device.DevSensors['TivaTemp'] < 0:
            self.label_tiva_temp.setText("Read Failed!")
        else:
            self.label_tiva_temp.setText(str(self.device.DevSensors['TivaTemp']))
        if self.device.DevSensors['PhotoDetector'] < 0:
            self.label_grren_val.setText("Read Failed!")
        else:
            self.label_grren_val.setText(str(self.device.DevSensors['PhotoDetector']))

    def SetUiInfo(self):
        self._clear_plot()
        if self.device.IsConnected():
            self.label_connected.setText('Connected!')
            self.tabWidget.setTabEnabled(1, True)
            self.tabWidget_ScanSetting.setEnabled(True)
            # Scan Config
            self._populate_cfglist_comboBox()
            index = self.comboBox_scanID.currentIndex()
            self.spinBox_numRepeat.setValue(self.cfglist.TargetConfig[index][3])

            # Device information
            if self.device.Information() == 0:
                self.label_device_GUIver.setText(str(self.windowTitle())[-5:])
                self.label_device_TivaSWver.setText(str(self.device.DevInfo['TivaRev']).strip('[]').replace(',', '.'))
                self.label_device_DLPCver.setText(str(self.device.DevInfo['DLPCRev']).strip('[]').replace(',', '.'))
                self.label_device_SpectrumLibVer.setText(str(self.device.DevInfo['SpecLibVer']).strip('[]').replace(',', '.'))
                self.label_device_MBver.setText(str(self.device.DevInfo['HWRev'][0]))
                self.label_device_DBver.setText(str(self.device.DevInfo['HWRev'][2]))
                self.label_device_ModelName.setText(self.device.DevInfo['ModelName'])
                self.label_device_SerialNumber.setText(self.device.DevInfo['SerialNumber'])
                self.label_device_ManufSer.setText(self.device.DevInfo['Manufacturing_SerialNumber'])
                self.label_device_UUID.setText(self.device.DevInfo['DeviceUUID'])
            else:
                self.ErrorMsg("Connot Read Device Info")
        else:
            self.label_connected.setText("Not Connected!")
            self.tabWidget.setTabEnabled(1, False)
            self.tabWidget_ScanSetting.setEnabled(False)

        # Activation Key
        self._activation_enable()

        #Disable some buttons
        self.pushButton_eeprom_write_generic.setEnabled(False)
        self.pushButton_eeprom_restore_default.setEnabled(False)
        self.pushButton_eeprom_write.setEnabled(False)
        self.pushButton_tiva_fw_usb_update.setEnabled(False)
        self.pushButton_dlpc_fw_update.setEnabled(False)
        self.lineEdit_tiva_fw_filename.clear()
        self.lineEdit_dlpc_fw_filename.clear()
        self.lineEdit_key_number.clear()
        self.lineEdit_pix2wave0.clear()
        self.lineEdit_pix2wave1.clear()
        self.lineEdit_pix2wave2.clear()
        self.lineEdit_shiftVect0.clear()
        self.lineEdit_shiftVect1.clear()
        self.lineEdit_shiftVect2.clear()
        self.lineEdit_ModelName_utl.clear()
        self.lineEdit_SerNumber_utl.clear()
        self.lineEdit_DateTime_utl.clear()
        self.lineEdit_LampUsage_utl.clear()
        self.label_errStatus.clear()

    #Private methods
    def _populate_cfglist_comboBox(self):
        self.comboBox_scanID.clear()
        self.comboBox_scanID.blockSignals(True)
        if self.cfglist.GetTargetConfigList() == 0:
            for i in range(self.cfglist.GetTargetConfigListNum()):
                self.comboBox_scanID.addItem(self.cfglist.TargetConfig[i][2])
            self.comboBox_scanID.setCurrentIndex(-1)
            self.comboBox_scanID.blockSignals(False)
            index = self.cfglist.GetTargetActiveScanIndex()
            if index < 0:
                index = 0
            else:
                self.comboBox_scanID.setCurrentIndex(index)

    def _activation_enable(self):
        self.actived = self.device.GetActivationResult()
        if self.actived == 1:
            self.label_keyActive.setText("Actived!")
            self.groupBox_lampusage.setEnabled(True)
            lampUsage = self.device.ReadLampUsage()
            self.label_device_LampUsage.setText(str(lampUsage))
            self.radioButton_Lamp_Stable_Time.setEnabled(True)
            self.lineEdit_lamp_stable_time.setEnabled(True)
        else:
            self.label_keyActive.setText("Inactived!")
            self.groupBox_lampusage.setEnabled(False)
            self.label_device_LampUsage.setText('')
            self.radioButton_Lamp_Stable_Time.setEnabled(False)
            self.lineEdit_lamp_stable_time.setEnabled(False)

    def _timeout(self):
        if self.device.IsConnected() != 1:
            self.device.Init()
            ret = self.device.Open()
            print(ret)
            if ret == 0:
                time.sleep(1)
                self.SetUiInfo()
            else:
                self.label_connected.setText("Not Connected!")
                self.tabWidget.setTabEnabled(1, False)
                self.tabWidget_ScanSetting.setEnabled(False)

    def _chartView(self):
        self.chart = QtChart.QChart()

        axisX = QtChart.QCategoryAxis(labelsPosition=QtChart.QCategoryAxis.AxisLabelsPositionOnValue, startValue=900.0)
        axisX.setTitleText("Wavelength (nm)")
        axisX.setRange(900, 1700)
        axisX.setTickCount(9)
        axisX.setLabelsFont(QtGui.QFont("Times", 12))
        axisX.append("900", 900.0)
        axisX.append("1000", 1000)
        axisX.append("1100", 1100)
        axisX.append("1200", 1200)
        axisX.append("1300", 1300)
        axisX.append("1400", 1400)
        axisX.append("1500", 1500)
        axisX.append("1600", 1600)
        axisX.append("1700", 1700)
        self.chart.addAxis(axisX, QtCore.Qt.AlignBottom)

        self.axisY = QtChart.QValueAxis()
        self.axisY.setTitleText("Absorbance")
        self.axisY.setLabelFormat("%.2f")
        self.axisY.setRange(-5, 5)
        self.axisY.setLabelsFont(QtGui.QFont("Times", 12))
        self.chart.addAxis(self.axisY, QtCore.Qt.AlignLeft)
        self.chart.legend().setVisible(False)

        self.chartView = QtChart.QChartView(self.widget_plot)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chartView.sizePolicy().hasHeightForWidth())
        self.chartView.setSizePolicy(sizePolicy)
        self.chartView.setMinimumSize(680, 480)
        self.chartView.setMouseTracking(True)
        self.chartView.setAcceptDrops(False)
        self.chartView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.chartView.setObjectName("chartView")

        self.chartView.setChart(self.chart)

    def _plot(self):
        series = QtChart.QLineSeries()
        if self.radioButton_Absorbance.isChecked():
            if self.scan.WaveLength != [] and self.scan.Absorbance != []:
                self.axisY.setTitleText("Absorbance")
                self.axisY.setRange(-1, 5)
                for x, y in zip(self.scan.WaveLength, self.scan.Absorbance):
                    series.append(x, y)
        elif self.radioButton_Intensity.isChecked():
            if self.scan.WaveLength != [] and self.scan.Intensities != []:
                min_value = min(self.scan.Intensities)
                max_value = max(self.scan.Intensities)
                self.axisY.setTitleText("Intensity")
                self.axisY.setRange(min_value - 100, max_value + 100)
                for x, y in zip(self.scan.WaveLength, self.scan.Intensities):
                    series.append(x, y)
        elif self.radioButton_Reflectance.isChecked():
            if self.scan.WaveLength != [] and self.scan.Reflectance != []:
                self.axisY.setTitleText("Reflectance")
                self.axisY.setRange(-1, 1)
                for x, y in zip(self.scan.WaveLength, self.scan.Reflectance):
                    series.append(x, y)
        elif self.radioButton_Reference.isChecked():
            if self.scan.WaveLength != [] and self.scan.ReferenceIntensity != []:
                min_value = min(self.scan.ReferenceIntensity)
                max_value = max(self.scan.ReferenceIntensity)
                self.axisY.setTitleText("Reference")
                self.axisY.setRange(min_value - 1000, max_value * 1.1)
                for x, y in zip(self.scan.WaveLength, self.scan.ReferenceIntensity):
                    series.append(x, y)
        self.chart.addSeries(series)
        self.chart.setAxisY(self.axisY, series)
        self.chartView.setChart(self.chart)

    def _clear_plot(self):
        self.chart.removeAllSeries()

    def ErrorMsg(self, msg):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(msg)
        msgBox.exec_()
        ret = self.device.ReadErrorStatus()
        if ret == 0:
            if self.device.errStatus == 1:
                self.label_errStatus.setText(str(self.device.errCode))
            else:
                self.label_errStatus.clear()