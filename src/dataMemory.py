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
        assert(len(outputValueNames) == 1), 'Datamemory has only one output'
        assert(len(control) == 2), 'Datamemory should have 2 control signal inputs'
        assert(len(outputSignalNames) == 0), 'Datamemory should not have any control output'

        self.memory =self.memory
        self.memWrite = control[0][1]       # self.memWrite inneholder nå navnet til memory write keyen
        self.memRead = control[1][1]        # self.memRead inneholder nå navnet til memory read keyen
        self.address = inputSources[0][1]   # self.address inneholder nå navnet til inputen, som kan brukes for å hente output
        self.writeData = inputSources[1][1]
        
    def writeOutput(self):

        memReadControl = self.controlSignals[self.memRead]
        memWriteControl = self.controlSignals[self.memWrite]

        assert (memReadControl is int) or (memWriteControl is int), 'Neither control signals are valid'
        

        if memReadControl != 0:
            # Self.output skal være lik en eller annen addresse som skal ut av minne. 
            self.outputValues = self.memory[self.inputValues[self.address]]

        if memWriteControl != 0:
            # det kommer inn en verdi som skal skrives til data memory
            self.memory[self.address] = self.inputValues[self.writeData]

        # Remove this and replace with your implementation!
        raise AssertionError("writeOutput not implemented in class DataMemory!")
