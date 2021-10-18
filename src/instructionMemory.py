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

        self.inputName = inputSources[0][1]
        self.outputName = outputSignalNames[0]
        self.memory = super.memory
    
    def writeOutput(self):
        
        self.outputValues[self.outputName] = self.inputValues[self.inputName]   # Med antalgelse at instructionMemory.readInput() blir kjørt før dette, kan outputValues dictionariet få en key self.inputname, med verdi som ligger mappet til self.inputName i self.inputValues.