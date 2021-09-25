'''
Implements a simple CPU element for adding two integer operands.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement

class Add(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)
        
        assert(len(inputSources) == 2), 'Adder should have two inputs'
        assert(len(outputValueNames) == 1), 'Adder has only one output'
        assert(len(control) == 0), 'Adder should not have any control signal'
        assert(len(outputSignalNames) == 0), 'Adder should not have any control output'
        
        self.outputName = outputValueNames[0]
  
    def writeOutput(self):
        total_sum = 0
        for k in self.inputValues:
            assert(isinstance(self.inputValues[k], int) or isinstance(self.inputValues[k], int))
            total_sum += self.inputValues[k]

        self.outputValues[self.outputName] = total_sum & 0xffffffff  # Convert to 32-bit (ignore overflow)
