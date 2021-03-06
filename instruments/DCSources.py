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

class SIM928(Instrument):
	ch1Value = Float(0.0).tag(desc="Ch 1 Voltage (V)")
	ch2Value = Float(0.0).tag(desc="Ch 2 Voltage (V)")
	ch3Value = Float(0.0).tag(desc="Ch 3 Voltage (V)")

class TekAFG3022B(DCSource):
	outputRange = Enum(1e-3, 10e-3, 100e-3, 200e-3, 1.0, 10.0, 20.0).tag(desc='Output range')
	channel = Int(2).tag(desc='Tek channel')
	width = Float(10.0).tag(desc='Pulse width (ns)')

	def json_encode(self, matlabCompatible=False):
		jsonDict = super(TekAFG3022B, self).json_encode(matlabCompatible)
		jsonDict['channel'] = jsonDict.pop('channel')
		jsonDict['width'] = jsonDict.pop('width')
		if matlabCompatible:
			jsonDict['range'] = jsonDict.pop('outputRange')
		return jsonDict
