'''
Implements a CPU element for shifting a number two bits to the left
'''
from cpuElement import CPUElement
import common

class shiftLeftTwo(CPUElement):

    def connect(self, inputSource, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSource, outputValueNames, control, outputSignalNames)
        
        assert(len(inputSource) == 1),          'shiftLeftTwo should have one input'
        assert(len(outputValueNames) == 1),     'shiftLeftTwo has only one output'
        assert(len(control) == 0),              'shiftLeftTwo has no control signal'
        assert(len(outputSignalNames) == 0),    'ShiftLeftTwo should not have an output control signal' 

        self.outputName = outputValueNames[0]

    def writeOutput(self):
        self.inputValues *= 4

        self.outputValues[self.outputName] = self.inputValues
