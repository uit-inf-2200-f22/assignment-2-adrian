'''
Implements CPU element for Data Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''
import unittest
from cpuElement import CPUElement
from testElement import TestElement
from memory import Memory
import common

class DataMemory(Memory):
    def __init__(self, filename):
        Memory.__init__(self, filename)
        
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)
        
        assert(len(inputSources) == 2),         'Datamemory should have 2 inputs'
        assert(len(outputValueNames) == 1),     'Datamemory has only one output'
        assert(len(control) == 2),              'Datamemory should have 2 control signal inputs'
        assert(len(outputSignalNames) == 0),    'Datamemory should not have any control output'

        self.memory = self.memory
        self.memWrite = control[0][1]           # self.memWrite inneholder nå navnet til memory write keyen
        self.memRead = control[1][1]            # self.memRead inneholder nå navnet til memory read keyen
        self.outputName = outputValueNames[0]   # self.outputName inneholder nå navnet på verdien som skal ut av memory
        self.address = inputSources[0][1]       # self.address inneholder nå navnet til inputen, som kan brukes for å hente output
        self.writeData = inputSources[1][1]
        
    def writeOutput(self):
        print("Writing output for dataMemory...\n")
        memReadControl = self.controlSignals[self.memRead]
        memWriteControl = self.controlSignals[self.memWrite]

        if memReadControl == 1 and memWriteControl == 0:
            self.outputValues[self.outputName] = self.memory[self.inputValues[self.address]]

        if memWriteControl == 1 and memReadControl == 0:
            self.memory[self.address] = self.inputValues[self.writeData]

class TestDataMemory(unittest.TestCase):
    def setUp(self, memoryFile):
        self.testInput = TestElement()
        self.dataMemory = DataMemory(memoryFile)
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['address', 'writeData'],
            [],
            ['memWrite', 'memRead']
        )
        self.dataMemory.connect(
            [(self.testInput, 'address'),(self.testInput, 'writeData')],
            ['readData'],
            [(self.testInput, 'memWrite'), (self.testInput, 'memRead')],
            []
        )
        self.testOutput.connect(
            [(self.dataMemory, 'readData')],
            [],
            [],
            []
        )

    def test_correct_behaviour(self):
        print("========TESTING DM========")
        print("MEMREAD...")
        print("loaded on mem: 95")
        print("memWrite: 0\tmemRead: 1")
        self.dataMemory.memory = {266481593 : 95}
        self.testInput.setOutputValue('address', 266481593)
        self.testInput.setOutputValue('writeData', 102)
        self.testInput.setControlSignals('memWrite', 0)
        self.testInput.setControlSignals('memRead', 1)

        self.dataMemory.readInput()
        self.dataMemory.readControlSignals()
        self.dataMemory.writeOutput()

        self.testOutput.readInput()
        print("output: ", self.testOutput.inputValues['readData'])
        print("")

        print("MEMWRITE...")
        print("data to write: 102")
        print("memWrite: 1\tmemRead: 0")
        self.testInput.setOutputValue('address', 266481593)
        self.testInput.setOutputValue('writeData', 102)
        self.testInput.setControlSignals('memWrite', 1)
        self.testInput.setControlSignals('memRead', 0)

        self.dataMemory.readInput()
        self.dataMemory.readControlSignals()
        self.dataMemory.writeOutput()

        self.testOutput.readInput()
        print("on address: ", self.dataMemory.memory['address'])
        print("==========================\n")
