from instruments.AWGBase import AWG, AWGDriver
from atom.api import Int, Constant

from TekPattern import *

class Tek7000(AWG):
	numChannels = Int(default=2)
	seqFileExt = Constant('.awg')
	translator = Constant('TekPattern')
