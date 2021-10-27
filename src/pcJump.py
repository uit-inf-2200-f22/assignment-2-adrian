'''
Implements a cpu element for joining the upper 4 bits of the pc+4 
'''

import unittest
from testElement import TestElement
from cpuElement import CPUElement

class pcJump(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2),         'pcJump should have 2 inputs'
        assert(len(outputValueNames) == 1),     'pcJump only has one output'
        assert(len(control) == 0),              'pcJump has no control signal inputs'
        assert(len(outputSignalNames) == 0),    'pcJump does not have any control signal outputs'

        self.lstInput = inputSources[0][1]
        self.adderInput = inputSources[1][1]
        
        self.jumpAddress = outputValueNames[0]

    def writeOutput(self):
        dataA = f'{self.inputValues[self.lstInput]:028b}'
        dataB = f'{self.inputValues[self.adderInput]:032b}'[0:4]    # compressed way to get the first(last) 4 bits in the add
        print(dataA)
        print(dataB)
        print(dataB + dataA)
        self.outputValues[self.jumpAddress] = int(dataB + dataA,2)

class TestPcJump(unittest.TestCase):
    def setUp(self):
        self.testInput = TestElement()
        self.pcJump = pcJump()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['lstInput','adderInput'],
            [],
            []
        )
        self.pcJump.connect(
            [(self.testInput, 'lstInput'), (self.testInput, 'adderInput')],
            ['jumpAddress'],
            [],
            []
        )
        self.testOutput.connect(
            [(self.pcJump, 'jumpAddress')],
            [],
            [],
            []
        )

    def test_correct_behaviour(self):
        self.testInput.setOutputValue('lstInput', int('1010000000000000000000000000',2))
        self.testInput.setOutputValue('adderInput', int('11000000000000000000000000000000',2))

        self.pcJump.readInput()
        self.pcJump.writeOutput()

        self.testOutput.readInput()

        print("output: ", self.testOutput.inputValues['jumpAddress'])
        assert(self.testOutput.inputValues['jumpAddress'] == int('11001010000000000000000000000000',2   )), 'output value does not mactch excpected result'
        