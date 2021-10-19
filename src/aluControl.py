'''
Implements an alu (arithemtic logic unit) control unit for controling the alu
'''
from cpuElement import CPUElement

class aluControl(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1),         'aluControl should have only one input'
        assert(len(outputValueNames) == 0),     'aluControl should not have any outputs'
        assert(len(control) == 1),              'aluControl should have one control input'
        assert(len(outputSignalNames) == 1),    'aluControl should have one control signal output' 

        self.controlName = inputSources[0][1]

    def writeOutput(self):
        controlSignal = self.inputValues[self.controlName]
        
        if controlSignal == 0:
            self.outputValues = 1
            # Needs work currently