import PulseShapes
import Channels
import operator

from math import pi, sin, cos, acos, sqrt
import numpy as np
from JPMPulseSequencer import JPMPulse, JPMTAPulse
from functools import wraps

def overrideDefaults(chan, updateParams):
    '''Helper function to update any parameters passed in and fill in the defaults otherwise.'''
    #The default parameter list depends on the channel type so pull out of channel
    #First get the default or updated values
    paramDict = chan.pulseParams.copy()
    paramDict.update(updateParams)
    # pull in the samplingRate from the physicalChannel
    paramDict['samplingRate'] = chan.physChan.samplingRate
    return paramDict


def JPMBias (jpm, label='JPMBias', **kwargs):
    params = overrideDefaults(jpm, kwargs)
    return JPMPulse(label, jpm, params)

def JPMId(jpm, *args, **kwargs):
    '''
    A delay or no-op in the form of a pulse.
    Accepts the following pulse signatures:
        Id(qubit, [kwargs])
        Id(qubit, delay, [kwargs])
        Id(qubit1, qubit2, [kwargs])
        Id((qubit1,qubit2...), delay, [kwargs])
    '''
    params = overrideDefaults(jpm, kwargs)
    if len(args) > 0 and isinstance(args[0], (int,float)):
        params['length'] = args[0]

    return JPMTAPulse("JPMId", jpm, params['length'], 0)

def JPMMEAS(*args, **kwargs):
    '''
    JPMMEAS(jpm1, ...) constructs a measurement pulse block of a measurment
    Use the single-argument form for an individual readout channel, e.g.
        JPMMEAS(q1)
    Use tuple-form for joint readout, e.g.
        JPMMEAS((q1, q2))
    Use multi-argument form for joint simultaneous readout.
    '''
    def create_meas_pulse(jpm):
        if isinstance(jpm, Channels.JPM):
            #Deal with single qubit readout channel
            channelName = "M-" + jpm.label
        elif isinstance(jpm, tuple):
            #Deal with joint readout channel
            channelName = "M-"
            for q in jpm:
                channelName += q.label
        measChan = Channels.JPMMeasFactory(channelName)
        params = overrideDefaults(measChan, kwargs)
        params['frequency'] = params.pop('frequency')
        params['baseShape'] = params.pop('shapeFun')
        params['shapeFun'] = PulseShapes.autodyne
        if 'phase' in kwargs:
            phase = kwargs['phase']
        else:
            phase = 0.0


        return JPMPulse("JPMMEAS", measChan, params)

    return reduce(operator.mul, [create_meas_pulse(jpm) for jpm in args])
