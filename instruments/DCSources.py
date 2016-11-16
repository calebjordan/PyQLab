from atom.api import Str, Int, Float, Bool, Enum

from .Instrument import Instrument

class DCSource(Instrument):
	output = Bool(False).tag(desc='Output enabled')
	mode = Enum('voltage', 'current').tag(desc='Output mode (current or voltage source)')
	value = Float(0.0).tag(desc='Output value (current or voltage)')

class YokoGS200(DCSource):
	outputRange = Enum(1e-3, 10e-3, 100e-3, 200e-3, 1, 10, 30).tag(desc='Output range')

	def json_encode(self, matlabCompatible=False):
		jsonDict = super(YokoGS200, self).json_encode(matlabCompatible)
		if matlabCompatible:
			jsonDict['range'] = jsonDict.pop('outputRange')
		return jsonDict

class SIM928(DCSource):
	outputRange = Enum(1e-3, 10e-3, 100e-3, 200e-3, 1.0, 10.0, 20.0).tag(desc='Output range')
	channel = Int(3).tag(desc='SIM channel {2,3}')

	def json_encode(self, matlabCompatible=False):
		jsonDict = super(SIM928, self).json_encode(matlabCompatible)
		jsonDict['channel'] = jsonDict.pop('channel')
		if matlabCompatible:
			jsonDict['range'] = jsonDict.pop('outputRange')
		return jsonDict
