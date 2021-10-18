'''
Implements CPU element for Data Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
from memory import Memory
import common

class DataMemory(Memory):
    def __init__(self, filename):
        Memory.__init__(self, filename)
        
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)
        
        assert(len(inputSources) == 2), 'Datamemory should have 2 inputs'
        assert(len(outputValueNames) == 1), 'Datamemory has only one input'
        assert(len(control) == 2), 'Datamemory should have 2 control signals'
        assert(len(outputSignalNames) == 0), 'Datamemory should not have any control output'

        self.memory = super.memory
        
    def writeOutput(self):
        # Remove this and replace with your implementation!
        raise AssertionError("writeOutput not implemented in class DataMemory!")
