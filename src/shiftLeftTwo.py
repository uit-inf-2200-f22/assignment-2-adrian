'''
Implements a CPU element for shifting a number two bits to the left
'''
from cpuElement import CPUElement
import common

class ShiftLeftTwo(CPUElement):

    def connect(self, inputSource, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSource, outputValueNames, control, outputSignalNames)
        
        assert(len(inputSource) == 1),          'shiftLeftTwo should have one input'
        assert(len(outputValueNames) == 1),     'shiftLeftTwo has only one output'
        assert(len(control) == 0),              'shiftLeftTwo has no control signal'
        assert(len(outputSignalNames) == 0),    'ShiftLeftTwo should not have an output control signal' 

        self.inputName = inputSource[0][1]
        self.outputName = outputValueNames[0]

    def writeOutput(self):
        # print("Writing output for shiftLeftTwo...\n")
        output = self.inputValues[self.inputName] * 4

        self.outputValues[self.outputName] = output
