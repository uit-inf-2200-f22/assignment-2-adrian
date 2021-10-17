'''
Implements an arithmetic logic unit
'''
from cpuElement import CPUElement

class Alu(CPUElement):

    def connect(self, input, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, input, outputValueNames, control, outputSignalNames)

        assert (len(input) == 2), 'Alu should have 2 inputs'
        assert (len(outputValueNames) == 1), 'Alu should have 1 output'
        assert (len(control) == 1), 'Alu should have 1 control input'
        assert (len(outputValueNames) == 1), 'Alu should have 1 control output'

        self.inputValue = input
        self.controlSignal = control
    
    def writeOutput(self):
        src, signal = self.controlSignal

        # Do something based on the control signal
        if signal == 100:
            return