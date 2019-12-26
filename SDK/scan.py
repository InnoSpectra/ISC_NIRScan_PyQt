from . import iscpy as isc

class Scan:
	def __init__(self):
		self.errMessage = ""
		self.isReadBinFile = False
		self.WaveLength = []
		self.Intensity = []
		self.Absorbance = []
		self.Reflectance = []
		self.scanDataLen = 0
		self.PGA = 0
		self.scanConfig = ()
		self.scanDateTime = []
		self.scanSensor = []
		self.ReferenceIntensity = []
		self.RefScanConfig = ()
		self.RefPGA = 0
		self.RefScanDateTime = []
		self.RefScanSensor = [] 

	def SetLamp(self, control):
		ret = -1
		if not isinstance(control, int) or control < 0 or control > 2:
			return ret
		isc.SetLamp(control)
		ret = 0
		return ret

	def SetLampDelay(self, time):
		ret = -1
		if not isinstance(time, int):
			return ret
		ret = isc.SetLampDelay(time)
		return ret

	def GetEstimatedScanTime(self):
		result = isc.GetEstimatedScanTime()
		return result

	def SetScanNumRepeats(self, repeat):
		ret = -1
		if not isinstance(repeat, int):
			return ret
		result = isc.SetScanNumRepeats(repeat)
		return result

	def SetFixedPGAGain(self, isFixed, gainVal):
		ret = -1
		if not (isinstance(isFixed, bool) and isinstance(gainVal, int)):
			return ret
		ret = isc.SetFixedPGAGain(isFixed, gainVal)
		return ret

	def SetPGAGain(self, gainVal):
		ret = -1
		if not isinstance(gainVal, int):
			return ret
		try:
			ret = isc.SetPGAGain(gainVal)
		except:
			print(ret)
		return ret

	def GetPGAGain(self):
		ret = isc.GetPGAGain()
		return ret

	def EnableGlitchFilter(self, enable):
		ret = -1
		if not isinstance(enable, bool):
			return ret
		ret = isc.EnableGlitchFilter(enable)
		return ret

	def ReadGlitchFilterStatus(self, enable):
		ret = -1
		if not isinstance(enable, bool):
			return ret
		ret = isc.ReadGlitchFilterStatus(enable)
		return ret

	def PerformScan(self, refSelect):
		ret = -1
		if not isinstance(refSelect, int) or refSelect < 0 or refSelect > 2:
			return ret
		ret = isc.PerformScan(refSelect)
		return ret

	def GetScanDataLength(self):
		self.scanDataLen = isc.GetScanDataLength()

	def GetRefScanPGAGain(self):
		ret = isc.GetRefScanPGAGain()
		return ret

	def GetScanResult(self):
		self.WaveLength = isc.GetWavelengths()
		self.Intensities = isc.GetIntensities()
		self.Absorbance = isc.GetAbsorbance()
		self.Reflectance = isc.GetReflectance()
		self.ReferenceIntensity = isc.GetRefIntensities()
		self.PGA = self.GetPGAGain()
		self.RefPGA = self.GetRefScanPGAGain()

	def SaveReferenceScan(self):
		ret = isc.SaveReferenceScan()
		return ret

	def IsLocalReferenceExist(self):
		ret = isc.IsLocalReferenceExist()
		return ret

	def GetScanConfig(self):
		ret = -1
		result = isc.GetScanConfig()
		self.scanConfig = ()
		if not isinstance(result, tuple):
			return ret
		ret = 0
		self.scanConfig = result
		return ret

	def GetScanDateTime(self):
		self.scanDateTime = []
		ret, result = isc.GetScanDateTime()
		if ret == 0:
			self.scanDateTime = result
		return ret

	def GetScanSensorData(self):
		self.scanSensor = []
		ret, result = isc.GetScanSensorData()
		if ret == 0:
			self.scanSensor = result
		return ret

	def GetRefScanConfig(self):
		self.RefScanConfig =()
		ret, result = isc.GetRefScanConfig()
		if ret == 0:
			self.RefScanConfig = result
		return ret

	def GetRefScanDateTime(self):
		self.RefScanDateTime = []
		ret, result = isc.GetRefScanDateTime()
		if ret == 0:
			self.RefScanDateTime = result
		return ret

	def GetRefScanSensorData(self):
		self.RefScanSensor = []
		ret, result = isc.GetRefScanSensorData()
		if ret == 0:
			self.RefScanSensor = result
		return ret	

	def SaveScanResultToBinFile(self, filename):
		ret = -1
		if not isinstance(filename, str):
			return ret
		ret = isc.SaveScanResultToBinFile(filename)
		return ret

	def ReadScanResultFromBinFile(self, filename):
		ret = -1
		if not isinstance(filename, str):
			return ret
		ret = isc.ReadScanResultFromBinFile(filename)
		return ret