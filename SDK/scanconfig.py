from . import iscpy as isc

class ScanConfig:
	def __init__(self):
		self.errMessage = ""
		self.currentConfig = {}
		self.TargetConfigLen = 0
		self.TargetConfig = []
		self.ActCfgIdx = 0
		self.RefConfig = (2, "default", "RefCal", 30, 1, [(0, 6, 900, 1700, 228, 0)])
		self.configFormat = "config format: \n" + \
							" (int, str, str, int, int, [sections])\n" + \
							" section format: \n" + \
							" (int, int, int, int, int, int)"

	def _print_config_format(self):
		self.errMessage = "Please follow the required config format:\n" + self.configFormat

	def _validate_config(self, config):
		ret = -1
		if not isinstance(config, tuple) or len(config) != 6:
			self._print_config_format()
			return ret

		if not (isinstance(config[0], int) and isinstance(config[1], str) \
			and isinstance(config[2], str) and isinstance(config[3], int) \
			and isinstance(config[4], int) and isinstance(config[5], list)):
			self._print_config_format()
			return ret

		if len(config[1]) > 8 or len(config[2]) > 40:
			self.errMessage = "Invalid string length in serial number(8) or config name(40)"
			ret = -1
			return ret

		for section in config[5]:
			if not isinstance(section, tuple) or len(section) != 6:
				self._print_config_format()
				return ret

			if not (isinstance(section[0], int) and isinstance(section[1], int) \
				and isinstance(section[2], int) and isinstance(section[3], int) \
				and isinstance(section[4], int) and isinstance(section[5], int)):
				self._print_config_format()
				return ret

		ret = 0		
		return ret

	def GetTargetConfigListNum(self):
		result = isc.GetTargetConfigListNum()
		self.TargetConfigLen = result
		return result

	def GetTargetConfigList(self):
		ret = -1
		configLen = self.GetTargetConfigListNum()
		if configLen <= 0:
			return ret
		ret, result = isc.GetTargetConfigList()
		if ret == 0:
			self.TargetConfig = result
		return ret

	def SetConfigList(self, configList):
		ret = -1
		if(len(configList) > 20):
			self.errMessage = "Config list size over 20!"
		if not isinstance(configList, list):
			self.errMessage = "Require a list of configs as input"
			return ret

		for config in configList:
			ret = self._validate_config(config)
			if ret < 0:
				return ret

		ret = isc.SetTargetConfigList(configList)
		return ret

	def SetTargetActiveScanIndex(self, index):
		ret = -1
		if(type(index) != int):
			self.errMessage = "Index type is not an integer"
			return ret

		if index > self.TargetConfigLen:
			self.errMessage = "Set index out of range"

		ret = isc.SetActiveScanIndex(index)
		return ret

	def AddIntoTargetConfigList(self, config):
		ret = self._validate_config(config)
		if not ret < 0:
			self.TargetConfig.append(config)
			self.TargetConfigLen = self.TargetConfigLen+1
		return ret

	def EditTargetConfigList(self, config, index):
		ret = self._validate_config(config)
		if not ret < 0:
			try:
				self.TargetConfig[index] = config
			except:
				self.errMessage = "Valid config, invalid index"
				ret = -1
		return ret

	def DeleteConfig(self, index):
		try:
			del self.TargetConfig[index]
			self.TargetConfigLen = self.TargetConfigLen-1
		except:
			self.errMessage = "Invalid config index."
			return -1
		return 0

	def GetTargetActiveScanIndex(self):
		result = isc.GetActiveScanIndex()
		if result > 0:
			self.ActCfgIdx = result
		return result

	def GetMaxPatterns(self, config, section_idx):
		ret = self._validate_config(config)
		if ret < 0:
			self._print_config_format()
			return ret

		if not isinstance(section_idx, int) or section_idx < 0 or section_idx > 4:
			self.errMessage = "Section index out of range."
			ret = -1
			return ret

		section = config[5][section_idx]
		result = isc.GetMaxPatterns(config[2], section[0], section[2], \
									section[3], section[1], config[3])
		return result

	def SetScanConfig(self, config):
		ret = self._validate_config(config)
		if ret < 0:
			self._print_config_format()
			return ret

		ret = isc.SetScanConfig(config[0], config[1], config[2], config[3], \
										config[4], config[5])
		return ret
