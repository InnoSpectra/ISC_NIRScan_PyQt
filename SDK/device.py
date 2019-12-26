from . import iscpy as isc

class Device:
	def __init__(self):
		self.errMessage = ""
		self.deviceStatus = 0
		self.errStatus = 0
		self.lampUsage = 0
		self.serialNumber = ""
		self.errCode = []
		self.ShiftVectorCoeffs = ()
		self.PixelToWavelengthCoeffs = ()
		self.DevDateTime = {'Year': 0, 'Month': 0, 'Day': 0, 'DayOfWeek': 0, \
											'Hour': 0, 'Minute': 0, 'Second': 0}
		self.DevInfo = {'ModelName': "", 'SerialNumber': "", 'DeviceUUID': "", 'HWRev': [], \
						'TivaRev': [], 'DLPCRev': [], 'SpecLibVer': [], 'Manufacturing_SerialNumber': ""}
		self.DevSensors = {'BattStatus': "", 'BattCapicity': 0.0, 'Humidity': 0.0, 'HDCTemp': 0.0, \
						'TivaTemp': 0.0, 'PhotoDetector': 0}

	def Print(self):
		print("deviceStatus: ", self.deviceStatus)
		print("errStatus: ", self.errStatus)
		print("lampUsage: ", self.lampUsage)
		print("DevInfo: ", self.DevInfo)
		print("DevDateTime: ", self.DevDateTime)
		print("DevSensors: ", self.DevSensors)
		print("errCode: ", self.errCode)
		print("ShiftVectorCoeffs: ", self.ShiftVectorCoeffs)
		print("PixelToWavelengthCoeffs: ", self.PixelToWavelengthCoeffs)

	def Init(self):
		ret = isc.Init()
		return ret

	def Open(self):
		ret = isc.Open()
		return ret

	def Close(self):
		ret = isc.Close()
		return ret

	def Exit(self):
		ret = isc.Exit()
		return ret

	def IsConnected(self):
		ret = isc.IsConnected()
		return ret

	def Enumerate(self):
		ret, devices = isc.Enumerate()
		return ret, devices

	def ResetTiva(self):
		ret = isc.ResetDeviceTiva()
		if ret == 0:
			ret = isc.Close()
		return ret

	def ReadDeviceStatus(self):
		ret, result = isc.ReadDeviceStatus()
		self.deviceStatus = result
		return ret

	def Information(self):
		ret, result = isc.Information()
		if ret == 0:
			self.DevInfo['ModelName'] = result[0]
			self.DevInfo['SerialNumber'] = result[1]
			self.serialNumber = result[1]
			temp_uuid = result[2]
			if(len(temp_uuid) < 23):
				for i in range(7):
					if temp_uuid.find(':',i*3+2) != (i*3+2):
						temp_uuid = temp_uuid[:(i*3+2-2)] + '0' + temp_uuid[(i*3+2-2):]
			self.DevInfo['DeviceUUID'] = temp_uuid
			self.DevInfo['HWRev'] = result[3]
			TivaRev_arr = []
			TivaRev_arr.append((result[4] & 0x00ff0000) >> 16)
			TivaRev_arr.append((result[4] & 0x0000ff00) >> 8)
			TivaRev_arr.append((result[4] & 0x000000ff) >> 0)
			TivaRev_arr.append((result[4] & 0xff000000) >> 24)			
			self.DevInfo['TivaRev'] = TivaRev_arr
			DLPCREV_arr = []
			DLPCREV_arr.append((result[5] & 0xff000000) >> 24)
			DLPCREV_arr.append((result[5] & 0x00ff0000) >> 16)
			DLPCREV_arr.append((result[5] & 0x0000ff00) >> 8)				
			self.DevInfo['DLPCRev'] = DLPCREV_arr
			SpecLibVer_arr = []
			SpecLibVer_arr.append((result[6] & 0x00ff0000) >> 16)
			SpecLibVer_arr.append((result[6] & 0x0000ff00) >> 8)
			SpecLibVer_arr.append((result[6] & 0x000000ff) >> 0)
			SpecLibVer_arr.append((result[6] & 0xff000000) >> 24)				
			self.DevInfo['SpecLibVer'] = SpecLibVer_arr
			self.DevInfo['Manufacturing_SerialNumber'] = result[7]
		return ret

	def ReadErrorStatus(self):
		ret, result = isc.ReadErrorStatus()
		if ret == 0:
			self.errStatus = 0
			self.errCode = result[1]
		else:
			self.errStatus = 1
		return ret

	def ResetErrorStatus(self):
		ret = isc.ResetErrorStatus()
		if ret == 0:
			self.errStatus = 0
		return ret

	def SetBluetooth(self, enable):
		ret = -1
		if not isinstance(enable, bool):
			return ret

		ret = isc.SetBluetooth(enable)
		return ret

	def ChkBleExist(self):
		ret = isc.ChkBleExist()
		return ret

	def ReadSensorsData(self):
		result = isc.ReadSensorsData()
		self.DevSensors['BattStatus'] = result[0]
		self.DevSensors['BattCapicity'] = result[1]
		self.DevSensors['Humidity'] = result[2]
		self.DevSensors['HDCTemp'] = result[3]
		self.DevSensors['TivaTemp'] = result[4]
		self.DevSensors['PhotoDetector'] = result[5]

	def SetModelName(self, modelName):
		ret = -1
		if not isinstance(modelName, str) or len(modelName) > 30:
			self.errMessage = "Length of model name should be shorter than 30."
			return ret
		ret = isc.SetModelName(modelName)
		if ret == 0:
			self.DevInfo['ModelName'] = modelName
		return ret

	def ReadModelName(self):
		ret, result = isc.ReadModelName()
		if ret == 0:
			self.DevInfo['ModelName'] = result
		return ret

	def SetSerialNumber(self, serialNumber):
		ret = -1
		if not isinstance(serialNumber, str) or len(serialNumber) > 8:
			self.errMessage = "Length of serial number should be shorter than 8."
			return ret
		ret = isc.SetSerialNumber(serialNumber)
		if ret == 0:
			self.DevInfo['SerialNumber'] = serialNumber
		return ret

	def GetSerialNumber(self):
		ret, result = isc.GetSerialNumber()
		if ret == 0:
			self.DevInfo['SerialNumber'] = result
		return ret

	def SetDateTime(self, year, month, day, hour, minute, second):
		ret = -1
		dayofweek = int(4)
		if not (isinstance(year, int) and isinstance(month, int) and isinstance(day, int) and\
				isinstance(dayofweek, int) and isinstance(hour, int) and isinstance(minute, int) and\
				isinstance(second, int)):
			return ret

		ret = isc.SetDateTime(year, month, day, dayofweek, hour, minute, second)
		return ret

	def GetDateTime(self):
		ret, result = isc.GetDateTime()
		if ret == 0:
			self.DevDateTime['Year'] = result[0]
			self.DevDateTime['Month'] = result[1]
			self.DevDateTime['Day'] = result[2]
			self.DevDateTime['DayOfWeek'] = result[3]
			self.DevDateTime['Hour'] = result[4]
			self.DevDateTime['Minute'] = result[5]
			self.DevDateTime['Second'] = result[6]
		return ret

	def WriteLampUsage(self, usage):
		ret = -1
		if not isinstance(usage, int):
			return ret

		ret = isc.WriteLampUsage(usage)
		return ret

	def ReadLampUsage(self):
		ret, result = isc.ReadLampUsage()
		if ret == 0:
			self.lampUsage = result
		return ret

	def GetCalibStruct(self):
		ret, result = isc.GetCalibStruct()
		if ret == 0:
			self.PixelToWavelengthCoeffs = (result[0][0], result[0][1], result[0][2])
			self.ShiftVectorCoeffs = (result[1][0], result[1][1], result[1][2])
		return ret

	def SendCalibStruct(self, P2W, ShiftVec):
		ret = -1
		if not (isinstance(P2W, list) and isinstance(ShiftVec, list)):
			return ret

		if len(P2W) != 3:
			self.errMessage = "Invalid pixel to wavelength coefficients input!"
			return ret

		if len(ShiftVec) != 3:
			self.errMessage = "Invalid Shift vector coefficients input!"
			return ret

		ret = isc.SendCalibStruct(P2W[0], P2W[1], P2W[2], ShiftVec[0], ShiftVec[1], ShiftVec[2])
		return ret

	def SetGenericCalibStruct(self):
		ret = isc.SetGenericCalibStruct()
		return ret

	def RestoreDefaultCalibStruct(self):
		ret = isc.RestoreDefaultCalibStruct()
		return ret

	def DLPC_SetImageSize(self, imgSize):
		ret = isc.SetImageSize(imgSize)
		return ret

	def DLPC_CheckImageSignature(self, imgByteBuff):
		ret = isc.CheckImageSignature(imgByteBuff)
		return ret

	def DLPC_Update_WriteDate(self, imgByteBuff, byteToSend):
		ret = isc.FlashWriteData(imgByteBuff, byteToSend)
		return ret

	def DLPC_GetChecksum(self):
		ret, result = isc.GetFlashChecksum()
		if ret == 0:
			return result
		else:
			return ret

	def Tiva_SetTivaToBootloader(self):
		ret = isc.SetTivaToBootloader()
		return ret

	def Tiva_FWUpdate(self, filepath):
		filepath = filepath.replace('/', '//')
		print(filepath)

		ret = isc.TivaFWUpdate(filepath)

		return ret

	def BackupFactoryReference(self, serialNumber):
		ret = -1
		if not isinstance(serialNumber, str) or len(serialNumber) > 8:
			self.errMessage = "Length of serial number should be shorter than 8."
			return ret

		ret = isc.BackupFactoryReferenceToFile(serialNumber)

		return ret

	def RestoreFactoryReference(self, serialNumber):
		ret = -1
		if not isinstance(serialNumber, str) or len(serialNumber) > 8:
			self.errMessage = "Length of serial number should be shorter than 8."
			return ret

		ret = isc.RestoreFactoryReferenceFromFile(serialNumber)

		return ret

	def SetActivationKey(self, keyString):
		ret = -1
		if not isinstance(keyString, str):
			return ret

		keyString = keyString.replace(' ', '')
		if len(keyString) < 24:
			return ret
		keyArr = []

		if len(keyString) != 24:
			self.errMessage = "Invalid key input."
		for x in keyString:
			if x < '0' or (x > '9' and x < 'A') or x > 'F':
				self.errMessage = "Invalid key input."
				return ret

		for i in range(12):
			key = list(keyString[i*2:i*2+2])
			key[0] = (ord(key[0])-48) if key[0] <= '9' else (ord(key[0])-55)
			key[1] = (ord(key[1])-48) if key[1] <= '9' else (ord(key[1])-55)
			keyArr.append(key[0] * 16 + key[1])

		ret = isc.SetActivationKey(keyArr[0], keyArr[1], keyArr[2], keyArr[3], keyArr[4], keyArr[5], \
								keyArr[6], keyArr[7], keyArr[8], keyArr[9], keyArr[10], keyArr[11])
		return ret

	def ClearActivationKey(self):
		ret = isc.SetActivationKey(0,0,0,0,0,0,0,0,0,0,0,0)
		return ret

	def GetActivationResult(self):
		result = isc.GetActivationResult()
		return result