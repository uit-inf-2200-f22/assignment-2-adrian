'''
Implements CPU element for Instruction Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
from memory import Memory

class InstructionMemory(Memory):
    def __init__(self, filename):
        Memory.__init__(self, filename)
    
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)
        
        assert (len(inputSources) == 1), 'Instruction memory should only have 1 input'
        assert (len(outputValueNames) == 1), 'Instruction memory should only have 1 output'
        assert(len(control) == 0), 'Instruction memory should not have control input'
        assert (len(outputSignalNames) == 0), 'Instruction memory should not have any control outputs'

        self.memory = super.memory
    
    def writeOutput(self):
        


        return 1