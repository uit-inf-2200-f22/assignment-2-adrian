'''
Implements a cpuElement for an and-gate
'''
import unittest
from cpuElement import CPUElement
from testElement import TestElement

class And(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 0),         'And gate has no inputs'
        assert(len(outputValueNames) == 0),     'And gate has no outputs'
        assert(len(control) == 2),              'And gate has 2 control inputs'
        assert(len(outputSignalNames) == 1),    'And gate has 1 control signal output'

        self.controlInput = inputSources[0][1]
        self.zeroControl = inputSources[1][1]
        self.signalName = outputSignalNames[0]

    def setControlSignals(self):     
        control = self.controlSignals[self.controlInput] 
        zero = self.controlSignals[self.zeroControl]

        if control == 1 and zero == 1:
            self.outputControlSignals[self.signalName] = 1
        else:
            self.outputControlSignals[self.signalName] = 0
