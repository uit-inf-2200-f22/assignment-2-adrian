'''
Implements CP Element for control
'''

from cpuElement import CPUElement

class Control(CPUElement):
    
    def connect(self, input, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, input, outputValueNames, control, outputSignalNames)
        self.inputValues = input

    def writeOutput(self):
        pass # randomControl has no data output

    def setControlSignal(self):
        src, inputValue = self.inputValues
        
        # Do something depending on the input
        if inputValue == 103:
            return 0